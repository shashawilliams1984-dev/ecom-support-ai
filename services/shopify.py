import requests

SHOPIFY_STORE_URL = "your-store.myshopify.com"
SHOPIFY_ACCESS_TOKEN = "your_private_token"

def get_order(order_number):
    url = f"https://{SHOPIFY_STORE_URL}/admin/api/2023-10/orders.json"
    
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    orders = response.json().get("orders", [])

    for order in orders:
        if str(order["order_number"]) == str(order_number):
            return {
                "status": order["fulfillment_status"] or "Processing",
                "item": order["line_items"][0]["name"]
            }

    return None
