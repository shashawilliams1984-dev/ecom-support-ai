from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "AI Support Agent is LIVE"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ai")
async def ai_endpoint(request: Request):
    data = await request.json()
    message = data.get("message")

    if not message:
        return JSONResponse({"error": "No message provided"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Shopify customer support assistant."},
            {"role": "user", "content": message}
        ]
    )

    reply = response.choices[0].message.content

    return JSONResponse({
        "response": reply
    })

@app.get("/shopify")
def shopify_test():
    return {
        "status": "Shopify connection endpoint ready"
    }
