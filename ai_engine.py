

from openai import OpenAI

client = OpenAI()

def generate_ai_response(question):

    prompt = f"""
You are a helpful AI customer support agent for an e-commerce store.

Customer question:
{question}

Respond clearly and professionally.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
