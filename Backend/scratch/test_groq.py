import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {api_key[:10]}..." if api_key else "No API Key found")

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": "test"}]
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error Type:", type(e))
    print("Error Message:", str(e))
