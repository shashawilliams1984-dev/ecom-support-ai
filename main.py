from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# =========================
# ROOT (fixes "Not Found")
# =========================
@app.get("/")
def home():
    return {
        "status": "AI Support Agent is running",
        "message": "Backend is live on Render"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# AI ENDPOINT (basic)
# =========================
@app.post("/ai")
async def ai_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")

    # Simple logic (placeholder for real AI later)
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
