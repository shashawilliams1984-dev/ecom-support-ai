from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# REQUEST MODEL (IMPORTANT)
# =========================
class AIRequest(BaseModel):
    message: str


# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "Ecom Support AI is running"}


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# AI ENDPOINT (CLEAN + CONTROLLED)
# =========================
@app.post("/ai")
async def ai_endpoint(data: AIRequest):
    message = data.message

    if not message:
        return JSONResponse({
            "error": "No message provided"
        })

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Shopify customer support assistant. "
                        "Be concise, clear, and helpful. "
                        "Give short answers (maximum 2-3 sentences). "
                        "If order details are missing, ask for order number or email. "
                        "Do not give long explanations. "
                        "Respond like a professional support agent."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return {
            "response": completion.choices[0].message.content
        }

    except Exception as e:
        return JSONResponse({
            "error": str(e)
        })


# =========================
# SHOPIFY TEST ENDPOINT
# =========================
@app.get("/shopify")
def shopify_test():
    return {
        "status": "Shopify connection endpoint ready"
    }
