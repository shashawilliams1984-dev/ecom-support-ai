from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


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
# AI REQUEST MODEL
# =========================
class AIRequest(BaseModel):
    message: str


# =========================
# AI ENDPOINT
# =========================
@app.post("/ai")
def ai_endpoint(request: AIRequest):
    message = request.message

    if not message:
        return JSONResponse({
            "error": "No message provided"
        })

    return JSONResponse({
        "response": f"AI received: {message}"
    })


# =========================
# SHOPIFY TEST ENDPOINT
# =========================
@app.get("/shopify")
def shopify_test():
    return {
        "status": "Shopify connection endpoint ready"
    }
