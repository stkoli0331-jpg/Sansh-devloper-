import os
from google import genai

# GitHub Secrets se API key uthayega
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  print("Error: GEMINI_API_KEY nahi mili!")
else:
  # New Google GenAI Client initialize karna
  client = genai.Client(api_key=api_key)

  print("Sansh-devloper is scanning global markets for Micro-SaaS ideas...")

  # Gemini se high-income micro-SaaS analysis mangwana
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

  print("\n========================================")
  print("      SANSH-DEVLOGER MARKET REPORT      ")
  print("========================================")
  print(response.text)
  print("========================================")
  
