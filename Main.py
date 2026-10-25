import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  client = genai.Client(api_key=api_key)

  print("Sansh-devloper is connecting to Gemini...")

  response = client.models.generate_content(
      model="gemini-3.8-flash",
      contents=(
          "Hello Sansh-devloper! Write a 1-line powerful startup message for"
          " your cloud automation engine."
      ),
  )

  print("\n--- GEMINI AI OUTPUT ---")
  print(response.text)
  print("--------------------------")
  
