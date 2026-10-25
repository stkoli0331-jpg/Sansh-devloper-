import os
import google.generativeai as genai

# GitHub Secrets se API key uthayega
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  # Gemini ko configure karna
  genai.configure(api_key=api_key)

  # Model select karna
  model = genai.GenerativeModel("gemini-1.5-flash")

  # Gemini se message mangwana
  print("Sansh-devloper is connecting to Gemini...")
  response = model.generate_content(
      "Hello Sansh-devloper! Write a 1-line powerful startup message for your"
      " cloud automation engine."
  )

  print("\n--- GEMINI AI OUTPUT ---")
  print(response.text)
  print("--------------------------")
    
