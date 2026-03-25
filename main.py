from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# REQUEST MODEL
# =========================
class AIRequest(BaseModel):
    message: str


# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"status": "AI Support API running"}


# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# SHOPIFY TEST
# =========================
@app.get("/shopify")
def shopify_test():
    return {"message": "Shopify endpoint ready"}


# =========================
# AI CORE
# =========================
@app.post("/ai")
def ai_endpoint(request: AIRequest):
    user_message = request.message.lower()

    try:
        # =========================
        # SMART RULE LAYER
        # =========================

        if "refund" in user_message:
            return {
                "response": "I can help with that. Share your order number or purchase email so I can check your refund eligibility."
            }

        if "late" in user_message or "delayed" in user_message:
            return {
                "response": "Got it. Send your order number or email and I’ll check the latest delivery status right away."
            }

        if "where is my order" in user_message or "track" in user_message:
            return {
                "response": "I can track that for you. Provide your order number or the email used at checkout."
            }

        if "international" in user_message or "ship" in user_message:
            return {
                "response": "Yes, we ship internationally. Share your location and I’ll give you delivery time and cost."
            }

        # =========================
        # AI LAYER (ADVANCED TONE)
        # =========================
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a top-tier customer support agent for a premium Shopify store. "
                        "Be sharp, direct, and helpful. Maximum 2 sentences. "

                        "RULES: "
                        "- No fluff. No generic replies. "
                        "- Always guide the user to the next step. "
                        "- Speak with confidence like a real human agent. "

                        "GOAL: "
                        "Resolve the user's issue quickly and clearly."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.6,
            max_tokens=150,
        )

        ai_reply = response.choices[0].message.content.strip()

        return {"response": ai_reply}

    except Exception as e:
        return {"error": str(e)}
