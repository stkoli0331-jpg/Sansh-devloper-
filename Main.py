import os
import subprocess
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY nahi mili!")
else:
    client = genai.Client(api_key=api_key)
    print("Sansh-devloper is connecting with multi-model fallback...")

    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    success = False
    response_text = ""

    for model_name in models_to_try:
        print(f"Trying model: {model_name}...")
        max_retries = 3
        model_success = False
        
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=(
                        "Act as an elite software architect and frontend expert. Generate 1 high-value Micro-SaaS business idea. "
                        "Provide the output in two sections: First, write a detailed Market Report in Markdown. "
                        "Second, provide a clean, working Python script for a complete **Streamlit web application** (using `import streamlit as st`) "
                        "with interactive inputs, buttons, and a nice user interface inside a python code block."
                    )
                )
                response_text = response.text
                model_success = True
                break
            except Exception as e:
                print(f"Model {model_name} Attempt {attempt + 1} failed: {e}. Waiting 5 seconds...")
                time.sleep(5)
        
        if model_success:
            success = True
            print(f"Successfully generated using {model_name}!")
            break
        else:
            print(f"Model {model_name} exhausted retries, trying next model...")

    if success:
        with open("market_report.md", "w", encoding="utf-8") as f:
            f.write("# Sansh-devloper Autonomous Advanced MVP Report\n\n")
            f.write(response_text)

        code_marker = chr(96) * 3 + "python"
        end_marker = chr(96) * 3
        
        if code_marker in response_text:
            code_part = response_text.split(code_marker)[1].split(end_marker)[0]
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(code_part)
        else:
            with open("app.py", "w", encoding="utf-8") as f:
                f.write("import streamlit as st\nst.title('Sansh-devloper MVP')\nst.write('App ready!')")

        print("[SUCCESS] Advanced Streamlit files generated successfully!")

        subprocess.run(["git", "config", "--global", "user.name", "Sansh-devloper Bot"])
        subprocess.run(["git", "config", "--global", "user.email", "bot@sansh-devloper.local"])

        repo_url = f"https://x-access-token:{os.environ.get('GH_TOKEN')}@github.com/{os.environ.get('GITHUB_REPOSITORY')}.git"
        subprocess.run(["git", "remote", "set-url", "origin", repo_url])

        subprocess.run(["git", "add", "market_report.md", "app.py"])
        subprocess.run(["git", "commit", "-m", "🤖 AI Autonomous Update: Advanced Streamlit Web App MVP"])
        push_result = subprocess.run(["git", "push"])

        if push_result.returncode == 0:
            print("[SUCCESS] Files pushed to GitHub repo!")
        else:
            print("[WARNING] Git push failed.")
    else:
        print("Error: All models failed due to quota or server limits.")
        exit(1)
        
