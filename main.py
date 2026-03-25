from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from openai import OpenAI

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# OPENAI SETUP
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "AI Support Agent is LIVE"}

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# REQUEST MODEL
# =========================
class AIRequest(BaseModel):
    message: str

# =========================
# AI ENDPOINT (REAL AI)
# =========================
@app.post("/ai")
def ai_endpoint(request: AIRequest):
    message = request.message

    if not message:
        return JSONResponse({
            "error": "No message provided"
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Shopify customer support assistant. Answer clearly and professionally."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = response.choices[0].message.content

        return {
            "response": reply
        }

    except Exception as e:
        return {
            "error": str(e)
        }

# =========================
# SHOPIFY TEST ENDPOINT
# =========================
@app.get("/shopify")
def shopify_test():
    return {
        "status": "Shopify connection endpoint ready"
    }
