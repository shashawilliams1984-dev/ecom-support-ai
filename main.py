from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# =========================
# ROOT (THIS FIXES YOUR ISSUE)
# =========================
@app.get("/")
def home():
    return {"message": "AI Support Agent is LIVE"}


# =========================
# HEALTH CHECK (Render uses this)
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# TEST ROUTE
# =========================
@app.get("/test")
def test():
    return {"status": "working"}


# =========================
# SMART AI ENDPOINT (basic placeholder)
# =========================
@app.post("/ai")
async def ai_handler(request: Request):
    data = await request.json()
    
    user_message = data.get("message", "")

    # Simple logic (replace later with OpenAI)
    if "order" in user_message.lower():
        response = "Let me check your order status for you."
    elif "refund" in user_message.lower():
        response = "I can help you with a refund. Can you provide your order ID?"
    else:
        response = "I'm your AI support agent. How can I assist you today?"

    return JSONResponse(content={
        "user_message": user_message,
        "response": response
    })


# =========================
# OPTIONAL: SHOPIFY WEBHOOK (future use)
# =========================
@app.post("/webhook")
async def webhook_handler(request: Request):
    payload = await request.json()
    print("Webhook received:", payload)
    return {"status": "received"}
