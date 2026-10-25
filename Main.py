import os
import subprocess
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  client = genai.Client(api_key=api_key)
  print("Sansh-devloper is building the Micro-SaaS MVP and report...")

  max_retries = 5
  success = False
  report_text = ""
  code_text = ""

  for attempt in range(max_retries):
    try:
      # 1. Market Report generate karna
      response_report = client.models.generate_content(
          model="gemini-3.8-flash",
          contents=(
              "Act as an elite software architect. Generate 1 high-potential"
              " Micro-SaaS business idea including Project Name, Target"
              " Audience, and Core Feature in Markdown format."
          ),
      )
      report_text = response_report.text

      # 2. Working Python Code generate karna
      response_code = client.models.generate_content(
          model="gemini-3.8-flash",
          contents=(
              "Write a simple, clean, and working Python script for this"
              " Micro-SaaS idea. Provide ONLY valid Python code without extra"
              " explanation."
          ),
      )
      code_text = response_code.text
      success = True
      break
    except Exception as e:
      print(
          f"Attempt {attempt + 1} failed with error: {e}. Retrying in 10"
          " seconds..."
      )
      time.sleep(10)

  if success:
    # Local files save karna
    with open("market_report.md", "w", encoding="utf-8") as f:
      f.write(report_text)

    # Markdown backticks saaf karna agar code mein hon
    cleaned_code = code_text.replace("```python", "").replace("```", "")
    with open("app.py", "w", encoding="utf-8") as f:
      f.write(cleaned_code)

    print(
        "[SUCCESS] market_report.md and app.py generated and saved locally!"
    )

    # Git Configuration and Push
    print("Pushing generated files to GitHub repository...")
    subprocess.run(
        ["git", "config", "--global", "user.name", "Sansh-devloper Bot"]
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", "bot@sansh-devloper.local"]
    )

    repo_url = f"https://x-access-token:{os.environ.get('GH_TOKEN')}@github.com/{os.environ.get('GITHUB_REPOSITORY')}.git"
    subprocess.run(["git", "remote", "set-url", "origin", repo_url])

    subprocess.run(["git", "add", "market_report.md", "app.py"])
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "🤖 AI Autonomous Update: Generated Market Report & App MVP",
        ]
    )
    push_result = subprocess.run(["git", "push"])

    if push_result.returncode == 0:
      print("[SUCCESS] Both files successfully pushed to GitHub repo!")
    else:
      print("[WARNING] Git push failed.")
  else:
    print("Error: Server busy hone ki wajah se request poori nahi ho payi.")
    exit(1)
    
