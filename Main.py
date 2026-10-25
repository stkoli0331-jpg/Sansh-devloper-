import os

def run_sansh():
    print("Sansh Developer Core: Active")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Status: GEMINI_API_KEY not found in environment.")
    else:
        print("Status: GEMINI_API_KEY successfully detected!")
        print("Sansh-devloper is fully connected and ready for custom tasks.")

if __name__ == "__main__":
    run_sansh()
    
