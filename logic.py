

import re
from mock_data import orders
from ai_engine import generate_ai_response


def extract_order_number(text: str):
    match = re.search(r"\b\d{4,}\b", text)
    if match:
        return match.group(0)
    return None


def get_order(order_number: str):
    return orders.get(order_number)


def handle_order_question(question: str):
    order_number = extract_order_number(question)

    if not order_number:
        return {
            "intent": "order_tracking",
            "order_number": None,
            "order_status": None,
            "decision": "missing_order_number",
            "needs_human": False,
            "escalation_reason": None,
            "answer": "Please provide your order number."
        }

    order = get_order(order_number)

    if not order:
        return {
            "intent": "order_tracking",
            "order_number": order_number,
            "order_status": None,
            "decision": "order_not_found",
            "needs_human": True,
            "escalation_reason": "order_not_found",
            "answer": f"I could not find order {order_number}."
        }

    status = order.get("status")

    return {
        "intent": "order_tracking",
        "order_number": order_number,
        "order_status": status,
        "decision": "order_found",
        "needs_human": False,
        "escalation_reason": None,
        "answer": f"Order {order_number} status: {status}"
    }


def handle_refund_question(question: str):
    return {
        "intent": "refund_request",
        "order_number": None,
        "order_status": None,
        "decision": "manual_review",
        "needs_human": True,
        "escalation_reason": "refund_request",
        "answer": "Your refund request has been forwarded to a human agent."
    }


def handle_cancel_question(question: str):
    order_number = extract_order_number(question)

    return {
        "intent": "cancel_order",
        "order_number": order_number,
        "order_status": None,
        "decision": "manual_review",
        "needs_human": True,
        "escalation_reason": "manual_cancel_review",
        "answer": f"Cancellation status for order {order_number} requires manual review."
    }


def handle_question(question: str):
    question_lower = question.lower()

    if "refund" in question_lower:
        return handle_refund_question(question)

    if "cancel" in question_lower:
        return handle_cancel_question(question)

    if "order" in question_lower:
        return handle_order_question(question)

    ai_answer = generate_ai_response(question)

    return {
        "intent": "general_support",
        "order_number": None,
        "order_status": None,
        "decision": "ai_response",
        "needs_human": False,
        "escalation_reason": None,
        "answer": ai_answer
    }
