from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# 🔑 Replace with your real Groq API key
import os
from groq import Groq

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")


class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ New active model
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}
        from database import engine
import models

models.Base.metadata.create_all(bind=engine)