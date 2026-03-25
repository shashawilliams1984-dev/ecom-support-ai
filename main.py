from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# REQUEST MODEL
# =========================
class AIRequest(BaseModel):
    message: str


# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def home():
    return {"status": "AI Support API is running"}


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# SHOPIFY TEST ENDPOINT
# =========================
@app.get("/shopify")
def shopify_test():
    return {"message": "Shopify connection endpoint ready"}


# =========================
# AI ENDPOINT (CORE ENGINE)
# =========================
@app.post("/ai")
def ai_endpoint(request: AIRequest):
    user_message = request.message

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a high-performance AI customer support agent for a Shopify store. "
                        "You handle order tracking, refunds, shipping issues, and product questions. "

                        "RULES: "
                        "- Always be concise (max 2 sentences unless necessary). "
                        "- Sound like a real human support agent, not AI. "
                        "- Be confident, clear, and direct. "
                        "- Never ramble or over-explain. "

                        "ORDER HANDLING: "
                        "- If a customer asks about an order and gives NO details, ask for order number or email. "
                        "- If they provide details, respond as if you can access the order system. "
                        "- Give helpful next steps, not generic advice. "

                        "REFUNDS: "
                        "- Be calm and professional. "
                        "- Explain the process briefly and clearly. "

                        "TONE: "
                        "- Professional, helpful, slightly assertive. "
                        "- No fluff. No filler. No 'as an AI'. "
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=200,
        )

        ai_reply = response.choices[0].message.content.strip()

        return {"response": ai_reply}

    except Exception as e:
        return {"error": str(e)}
