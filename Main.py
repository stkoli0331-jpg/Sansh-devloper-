import os
import subprocess
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  client = genai.Client(api_key=api_key)
  print("Sansh-devloper is scanning global markets for Micro-SaaS ideas...")

  max_retries = 5
  success = False
  response_text = ""

  for attempt in range(max_retries):
    try:
      response = client.models.generate_content(
          model="gemini-3.8-flash",
          contents=(
              "Act as an elite software architect and startup strategist."
              " Generate 1 high-potential, scalable Micro-SaaS business idea that"
              " can be built with Python and AI APIs. Include: 1. Project Name, 2."
              " Target Audience, 3. Core Automation Feature, and 4. Monetization"
              " Strategy. Keep it sharp, structured, and powerful."
          ),
      )
      response_text = response.text
      success = True
      break
    except Exception as e:
      print(
          f"Attempt {attempt + 1} failed with error: {e}. Retrying in 10"
          " seconds..."
      )
      time.sleep(10)

  if success:
    filename = "market_report.md"
    with open(filename, "w", encoding="utf-8") as f:
      f.write("# Sansh-devloper Autonomous Market Report\n\n")
      f.write(response_text)
    print(f"\n[SUCCESS] Report generated and saved locally to {filename}!")

    # Configure Git and Push with Token
    print("Pushing report to GitHub repository...")
    subprocess.run(
        ["git", "config", "--global", "user.name", "Sansh-devloper Bot"]
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", "bot@sansh-devloper.local"]
    )

    # Repository URL mein token set karna taaki push block na ho
    repo_url = f"https://x-access-token:{os.environ.get('GH_TOKEN')}@github.com/{os.environ.get('GITHUB_REPOSITORY')}.git"
    subprocess.run(["git", "remote", "set-url", "origin", repo_url])

    subprocess.run(["git", "add", filename])
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "🤖 AI Autonomous Update: New Market Report Generated",
        ]
    )
    push_result = subprocess.run(["git", "push"])

    if push_result.returncode == 0:
      print("[SUCCESS] market_report.md successfully pushed to GitHub repo!")
    else:
      print("[WARNING] Git push failed.")

    print("\n--- GENERATED REPORT PREVIEW ---")
    print(response_text)
    print("--------------------------------")
  else:
    print("Error: Server busy hone ki wajah se request poori nahi ho payi.")
    exit(1)
    
