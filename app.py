
#!/usr/bin/env python3
"""
SpecDrift - API Contract & Breaking Change Sentinel
A production-ready Micro-SaaS MVP engine for tracking OpenAPI schema drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class ChangeEvent:
    severity: Severity
    endpoint: str
    method: str
    message: str


class Storage:
    """Handles persistence of specs, historical snapshots, and audit logs."""

    def __init__(self, db_path: str = "specdrift.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS watched_specs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    url TEXT NOT NULL,
                    auth_token TEXT,
                    last_hash TEXT,
                    last_checked_at TEXT
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spec_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    spec_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(spec_id) REFERENCES watched_specs(id)
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS drift_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    spec_id INTEGER NOT NULL,
                    severity TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    method TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(spec_id) REFERENCES watched_specs(id)
                );
            """)

    def add_spec(self, name: str, url: str, auth_token: Optional[str] = None) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO watched_specs (name, url, auth_token) VALUES (?, ?, ?);",
                (name, url, auth_token),
            )

    def list_specs(self) -> List[sqlite3.Row]:
        with self._get_connection() as conn:
            return conn.execute("SELECT * FROM watched_specs;").fetchall()

    def get_latest_snapshot(self, spec_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT content FROM spec_history WHERE spec_id = ? ORDER BY id DESC LIMIT 1;",
                (spec_id,),
            ).fetchone()
            if row:
                return json.loads(row["content"])
            return None

    def save_snapshot(
        self, spec_id: int, content: Dict[str, Any], content_hash: str
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO spec_history (spec_id, content, hash, created_at) VALUES (?, ?, ?, ?);",
                (spec_id, json.dumps(content), content_hash, now),
            )
            conn.execute(
                "UPDATE watched_specs SET last_hash = ?, last_checked_at = ? WHERE id = ?;",
                (content_hash, now, spec_id),
            )

    def log_drift(self, spec_id: int, event: ChangeEvent) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO drift_logs (spec_id, severity, endpoint, method, message, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?);",
                (spec_id, event.severity.value, event.endpoint, event.method, event.message, now),
            )


class SchemaDiffer:
    """Semantic comparison engine for OpenAPI v3.x schemas."""

    HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head"}

    @classmethod
    def diff(cls, old: Dict[str, Any], new: Dict[str, Any]) -> List[ChangeEvent]:
        events: List[ChangeEvent] = []
        old_paths = old.get("paths", {})
        new_paths = new.get("paths", {})

        # 1. Removed Endpoints (Breaking Change)
        for path in old_paths:
            if path not in new_paths:
                events.append(
                    ChangeEvent(
                        severity=Severity.CRITICAL,
                        endpoint=path,
                        method="*",
                        message=f"Endpoint entirely removed: {path}",
                    )
                )
                continue

            # Compare methods in existing paths
            old_methods = {
                m.lower(): old_paths[path][m]
                for m in old_paths[path]
                if m.lower() in cls.HTTP_METHODS
            }
            new_methods = {
                m.lower(): new_paths[path][m]
                for m in new_paths[path]
                if m.lower() in cls.HTTP_METHODS
            }

            # Method removals
            for method, definition in old_methods.items():
                if method not in new_methods:
                    events.append(
                        ChangeEvent(
                            severity=Severity.CRITICAL,
                            endpoint=path,
                            method=method.upper(),
                            message=f"Method {method.upper()} removed from endpoint {path}",
                        )
                    )
                else:
                    # Deep inspect parameters
                    cls._diff_parameters(
                        events, path, method, definition, new_methods[method]
                    )

        # 2. Added Endpoints (Additive Change)
        for path in new_paths:
            if path not in old_paths:
                events.append(
                    ChangeEvent(
                        severity=Severity.INFO,
                        endpoint=path,
                        method="*",
                        message=f"New endpoint introduced: {path}",
                    )
                )
            else:
                old_methods = {
                    m.lower() for m in old_paths[path] if m.lower() in cls.HTTP_METHODS
                }
                new_methods = {
                    m.lower() for m in new_paths[path] if m.lower() in cls.HTTP_METHODS
                }
                for method in new_methods - old_methods:
                    events.append(
                        ChangeEvent(
                            severity=Severity.INFO,
                            endpoint=path,
                            method=method.upper(),
                            message=f"New method {method.upper()} added to {path}",
                        )
                    )

        return events

    @staticmethod
    def _diff_parameters(
        events: List[ChangeEvent],
        path: str,
        method: str,
        old_op: Dict[str, Any],
        new_op: Dict[str, Any],
    ) -> None:
        old_params = {p.get("name"): p for p in old_op.get("parameters", []) if "name" in p}
        new_params = {p.get("name"): p for p in new_op.get("parameters", []) if "name" in p}

        # Check for newly added required parameters (Breaking)
        for p_name, p_data in new_params.items():
            if p_name not in old_params:
                if p_data.get("required") is True:
                    events.append(
                        ChangeEvent(
                            severity=Severity.CRITICAL,
                            endpoint=path,
                            method=method.upper(),
                            message=f"New required parameter added: '{p_name}'",
                        )
                    )
            else:
                # Existing param changed from optional to required (Breaking)
                was_req = old_params[p_name].get("required", False)
                now_req = p_data.get("required", False)
                if not was_req and now_req:
                    events.append(
                        ChangeEvent(
                            severity=Severity.CRITICAL,
                            endpoint=path,
                            method=method.upper(),
                            message=f"Existing parameter '{p_name}' became required",
                        )
                    )

        # Check for removed parameters
        for p_name in old_params:
            if p_name not in new_params:
                events.append(
                    ChangeEvent(
                        severity=Severity.WARNING,
                        endpoint=path,
                        method=method.upper(),
                        message=f"Parameter removed: '{p_name}'",
                    )
                )


class SpecEngine:
    """Core orchestrator for fetching, parsing, and dispatching checks."""

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def fetch_spec(self, url: str, auth_token: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "SpecDrift-Sentinel/1.0 (+https://specdrift.dev)")
        req.add_header("Accept", "application/json")
        if auth_token:
            req.add_header("Authorization", f"Bearer {auth_token}")

        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                raw_bytes = response.read()
                content_hash = hashlib.sha256(raw_bytes).hexdigest()
                parsed_json = json.loads(raw_bytes.decode("utf-8"))
                return parsed_json, content_hash
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error fetching spec at {url}: {e.reason}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Spec at {url} returned invalid JSON: {e}")

    def run_check(self, spec_row: sqlite3.Row) -> List[ChangeEvent]:
        spec_id = spec_row["id"]
        name = spec_row["name"]
        url = spec_row["url"]
        auth_token = spec_row["auth_token"]
        last_hash = spec_row["last_hash"]

        print(f"[*] Inspecting API '{name}' -> {url}")

        new_spec, current_hash = self.fetch_spec(url, auth_token)

        if current_hash == last_hash:
            print(f"[+] '{name}' is unchanged. Integrity intact.")
            return []

        previous_spec = self.storage.get_latest_snapshot(spec_id)

        if not previous_spec:
            print(f"[!] Baseline established for '{name}' (Hash: {current_hash[:8]}).")
            self.storage.save_snapshot(spec_id, new_spec, current_hash)
            return []

        events = SchemaDiffer.diff(previous_spec, new_spec)

        for event in events:
            self.storage.log_drift(spec_id, event)
            self._dispatch_alert(name, event)

        self.storage.save_snapshot(spec_id, new_spec, current_hash)
        return events

    def _dispatch_alert(self, spec_name: str, event: ChangeEvent) -> None:
        """Simulate webhook / notification dispatch (e.g., to Slack)."""
        color_map = {
            Severity.INFO: "\033[94m",     # Blue
            Severity.WARNING: "\033[93m",  # Yellow
            Severity.CRITICAL: "\033[91m", # Red
        }
        reset = "\033[0m"

        print(
            f"  {color_map[event.severity]}[{event.severity.value}]{reset} "
            f"[{spec_name}] {event.method} {event.endpoint} -> {event.message}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="specdrift",
        description="SpecDrift - OpenAPI Contract Drift & Breaking Change Sentinel",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Register a new API spec to monitor")
    add_parser.add_argument("--name", required=True, help="Friendly name of the API")
    add_parser.add_argument("--url", required=True, help="Public URL to openapi.json")
    add_parser.add_argument("--token", help="Bearer token for protected endpoints")

    # List command
    subparsers.add_parser("list", help="List all monitored APIs")

    # Scan command
    subparsers.add_parser("scan", help="Run drift detection across all monitored APIs")

    # Seed mock data
    subparsers.add_parser("seed-demo", help="Load test mock specs for verification")

    args = parser.parse_args()
    storage = Storage()
    engine = SpecEngine(storage)

    if args.command == "add":
        try:
            storage.add_spec(args.name, args.url, args.token)
            print(f"[+] Successfully added '{args.name}'. Run 'specdrift scan' to baseline.")
        except sqlite3.IntegrityError:
            print(f"[-] Error: Spec with name '{args.name}' already exists.")

    elif args.command == "list":
        specs = storage.list_specs()
        if not specs:
            print("No specifications registered. Use 'specdrift add' or 'specdrift seed-demo'.")
            return

        print(f"\n{'ID':<4} | {'Name':<15} | {'Last Checked':<25} | {'URL'}")
        print("-" * 75)
        for s in specs:
            checked = s["last_checked_at"] or "Never"
            print(f"{s['id']:<4} | {s['name']:<15} | {checked:<25} | {s['url']}")
        print()

    elif args.command == "scan":
        specs = storage.list_specs()
        if not specs:
            print("No targets configured.")
            return

        total_alerts = 0
        for s in specs:
            try:
                events = engine.run_check(s)
                total_alerts += len(events)
            except Exception as e:
                print(f"[-] Failed scanning '{s['name']}': {e}", file=sys.stderr)

        print(f"\nScan complete. Total drift signals dispatched: {total_alerts}")

    elif args.command == "seed-demo":
        # Simulates a baseline and modified API locally using raw dict comparison
        print("[*] Running localized verification test...")
        v1 = {
            "openapi": "3.0.0",
            "paths": {
                "/v1/payments": {
                    "post": {
                        "parameters": [
                            {"name": "amount", "required": True},
                            {"name": "currency", "required": False},
                        ]
                    }
                },
                "/v1/customers": {
                    "get": {"parameters": []}
                }
            }
        }

        v2 = {
            "openapi": "3.0.0",
            "paths": {
                "/v1/payments": {
                    "post": {
                        "parameters": [
                            {"name": "amount", "required": True},
                            {"name": "currency", "required": True},  # Broken: Now required
                            {"name": "tax_id", "required": True},    # Broken: New required param
                        ]
                    }
                },
                # /v1/customers was removed entirely (Broken)
                "/v1/subscriptions": {
                    "get": {"parameters": []}                 # Additive: New endpoint
                }
            }
        }

        diffs = SchemaDiffer.diff(v1, v2)
        print(f"\nVerification results ({len(diffs)} breaking/drift changes detected):")
        for d in diffs:
            print(f" -> [{d.severity.value}] {d.method} {d.endpoint}: {d.message}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
