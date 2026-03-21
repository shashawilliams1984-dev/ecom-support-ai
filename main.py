from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import re

from database import save_chat

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QuestionRequest(BaseModel):
    question: str
    session_id: str | None = None

# Fake DB
orders_db = {
    "12334": {"status": "Delivered", "item": "Black Hoodie", "refund_eligible": True},
    "56789": {"status": "In Transit", "item": "Running Shoes", "refund_eligible": False},
}

# Sessions
sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "intent": None,
            "order_number": None,
            "awaiting_reason": False
        }
    return sessions[session_id]

@app.post("/ask")
async def ask_question(payload: QuestionRequest):
    session_id = payload.session_id or str(uuid.uuid4())
    user_input = payload.question.lower()

    session = get_session(session_id)

    # STEP 1: detect intent
    if "refund" in user_input:
        session["intent"] = "refund"
        return {
            "answer": "Sure — I can help with a refund. Please provide your order number.",
            "session_id": session_id
        }

    # STEP 2: capture order number
    if session["intent"] == "refund" and not session["order_number"]:
        match = re.search(r"\d{4,}", user_input)
        if match:
            order_number = match.group()
            session["order_number"] = order_number

            if order_number not in orders_db:
                return {
                    "answer": "I couldn't find that order. Please check the number.",
                    "session_id": session_id
                }

            session["awaiting_reason"] = True
            return {
                "answer": f"Got it. What is the reason for your refund for order {order_number}?",
                "session_id": session_id
            }

    # STEP 3: capture reason
    if session["awaiting_reason"]:
        order = orders_db.get(session["order_number"])

        session["awaiting_reason"] = False

        if order["refund_eligible"]:
            return {
                "answer": f"Your refund for order {session['order_number']} has been approved. You will receive your money within 5–7 business days.",
                "session_id": session_id
            }
        else:
            return {
                "answer": f"Sorry, order {session['order_number']} is not eligible for a refund.",
                "session_id": session_id
            }

    # fallback
    return {
        "answer": "I can help with refunds. Try asking about a refund.",
        "session_id": session_id
    }
