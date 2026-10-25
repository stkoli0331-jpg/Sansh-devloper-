import os
import subprocess
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY nahi mili!")
else:
    client = genai.Client(api_key=api_key)
    print("Sansh-devloper is connecting to Gemini...")

    max_retries = 5
    success = False
    response_text = ""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=(
                    "Act as an elite software architect. Generate 1 Micro-SaaS business idea. "
                    "Provide the output in two sections: First, write the Market Report in Markdown. "
                    "Second, provide a clean, working Python script for the app inside a python code block."
                )
            )
            response_text = response.text
            success = True
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}. Waiting 10 seconds...")
            time.sleep(10)

    if success:
        with open("market_report.md", "w", encoding="utf-8") as f:
            f.write("# Sansh-devloper Autonomous MVP Report\n\n")
            f.write(response_text)

        # Clean Code Extraction without string formatting bugs
        code_marker = chr(96) * 3 + "python"
        end_marker = chr(96) * 3
        
        if code_marker in response_text:
            code_part = response_text.split(code_marker)[1].split(end_marker)[0]
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(code_part)
        else:
            with open("app.py", "w", encoding="utf-8") as f:
                f.write("# Fallback app script\nprint('Sansh-devloper MVP Ready!')")

        print("[SUCCESS] Files generated successfully!")

        subprocess.run(["git", "config", "--global", "user.name", "Sansh-devloper Bot"])
        subprocess.run(["git", "config", "--global", "user.email", "bot@sansh-devloper.local"])

        repo_url = f"https://x-access-token:{os.environ.get('GH_TOKEN')}@github.com/{os.environ.get('GITHUB_REPOSITORY')}.git"
        subprocess.run(["git", "remote", "set-url", "origin", repo_url])

        subprocess.run(["git", "add", "market_report.md", "app.py"])
        subprocess.run(["git", "commit", "-m", "🤖 AI Autonomous Update: Fast MVP Generation"])
        push_result = subprocess.run(["git", "push"])

        if push_result.returncode == 0:
            print("[SUCCESS] Files pushed to GitHub repo!")
        else:
            print("[WARNING] Git push failed.")
    else:
        print("Error: Request failed after retries.")
        exit(1)
      
