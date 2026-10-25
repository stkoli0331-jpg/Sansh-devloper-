import os

def run_sansh():
    print("Sansh Developer Core: Active")
    print("Connecting to AI Model...")
    
    # Yahan hum Gemini API key check kar rahe hain
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Status: API Key missing. Please set GEMINI_API_KEY.")
    else:
        print("Status: API Key detected. Ready for requests!")

if __name__ == "__main__":
    run_sansh()
    
