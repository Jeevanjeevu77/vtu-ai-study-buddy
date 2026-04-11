import os
import sys
from dotenv import load_dotenv
from groq import Groq

def check_groq_api():
    print("--- Groq API Diagnostic Tool ---")
    
    # Path to .env (assume current or parent directory)
    env_path = ".env"
    if not os.path.exists(env_path):
        env_path = os.path.join("..", ".env")
    
    if os.path.exists(env_path):
        print(f"[OK] Found .env file at: {os.path.abspath(env_path)}")
        load_dotenv(env_path, override=True)
    else:
        print("[ERROR] Could not find .env file!")
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("[ERROR] GROQ_API_KEY not found in environment!")
        return False
    
    print(f"[INFO] API Key starting with: {api_key[:10]}...")
    
    try:
        client = Groq(api_key=api_key)
        print("[WAIT] Testing connection to Groq...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print("[SUCCESS] AI Response:")
        print(f"   > {response.choices[0].message.content.strip()}")
        return True
    except Exception as e:
        print(f"[FAILED] Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        
        if "401" in str(e) or "AuthenticationError" in str(e):
            print("\nTIP: Your API key is invalid or expired.")
            print("   Get a new one at https://console.groq.com/keys")
        return False

if __name__ == "__main__":
    success = check_groq_api()
    sys.exit(0 if success else 1)
