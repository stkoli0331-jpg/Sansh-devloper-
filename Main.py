import os
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  client = genai.Client(api_key=api_key)
  print("Sansh-devloper is connecting to Gemini...")

  max_retries = 3
  success = False

  for attempt in range(max_retries):
    try:
      response = client.models.generate_content(
          model="gemini-1.5-flash",
          contents=(
              "Hello Sansh-devloper! Write a 1-line powerful startup message for"
              " your cloud automation engine."
          ),
      )
      print("\n--- GEMINI AI OUTPUT ---")
      print(response.text)
      print("--------------------------")
      success = True
      break
    except Exception as e:
      print(
          f"Attempt {attempt + 1} failed with error: {e}. Retrying in 5 seconds..."
      )
      time.sleep(5)

  if not success:
    print("Error: Server busy hone ki wajah se request poori nahi ho payi.")
    exit(1)
    
