from flask import Flask, render_template, request, jsonify
import re
from typing import List, Dict

app = Flask(__name__)

products = [
    {"id": 1, "name": "Galaxy A25", "brand": "Samsung", "category": "Phone", "price": 299, "tags": ["budget", "camera", "android"], "specs": {"camera": "50MP", "battery": "5000mAh"}},
    {"id": 2, "name": "Galaxy S24", "brand": "Samsung", "category": "Phone", "price": 799, "tags": ["premium", "camera", "5g"], "specs": {"camera": "200MP", "battery": "4000mAh"}},
    {"id": 3, "name": "Galaxy Tab A9", "brand": "Samsung", "category": "Tablet", "price": 219, "tags": ["budget", "travel", "tablet"], "specs": {"camera": "8MP", "battery": "5100mAh"}},
    {"id": 4, "name": "Galaxy Tab S9", "brand": "Samsung", "category": "Tablet", "price": 799, "tags": ["premium", "drawing", "tablet"], "specs": {"camera": "13MP", "battery": "8400mAh"}},
    {"id": 5, "name": "Q60D 55-inch TV", "brand": "Samsung", "category": "TV", "price": 549, "tags": ["tv", "gaming", "55-inch"], "specs": {"screen": "55-inch", "refresh": "60Hz"}},
    {"id": 6, "name": "QN90D 55-inch TV", "brand": "Samsung", "category": "TV", "price": 1299, "tags": ["tv", "gaming", "premium"], "specs": {"screen": "55-inch", "refresh": "120Hz"}},
    {"id": 7, "name": "Galaxy Book4 Pro", "brand": "Samsung", "category": "Laptop", "price": 1399, "tags": ["coding", "premium", "laptop"], "specs": {"cpu": "Intel Core Ultra", "ram": "16GB"}},
    {"id": 8, "name": "Galaxy Book4", "brand": "Samsung", "category": "Laptop", "price": 899, "tags": ["coding", "budget", "laptop"], "specs": {"cpu": "Intel Core", "ram": "8GB"}},
]


def extract_intents(query: str) -> Dict[str, object]:
    q = query.lower()
    category = None
    max_price = None
    min_price = None
    use_case = None
    budget = None

    if any(word in q for word in ["phone", "phones", "mobile"]):
        category = "Phone"
    elif any(word in q for word in ["tablet", "tab"]):
        category = "Tablet"
    elif any(word in q for word in ["tv", "television"]):
        category = "TV"
    elif any(word in q for word in ["laptop", "notebook", "computer"]):
        category = "Laptop"

    price_match = re.search(r"under\s*\$?(\d+)", q)
    if price_match:
        max_price = int(price_match.group(1))
    price_match = re.search(r"over\s*\$?(\d+)", q)
    if price_match:
        min_price = int(price_match.group(1))

    if any(word in q for word in ["budget", "affordable", "cheap"]):
        budget = "budget"
    elif any(word in q for word in ["premium", "high-end", "best"]):
        budget = "premium"

    if any(word in q for word in ["camera", "photo", "photography"]):
        use_case = "camera"
    elif any(word in q for word in ["gaming"]):
        use_case = "gaming"
    elif any(word in q for word in ["coding", "developer", "work"]):
        use_case = "coding"
    elif any(word in q for word in ["travel"]):
        use_case = "travel"
    elif any(word in q for word in ["drawing"]):
        use_case = "drawing"

    return {"category": category, "max_price": max_price, "min_price": min_price, "budget": budget, "use_case": use_case}


def rank_products(query: str) -> List[Dict[str, object]]:
    intents = extract_intents(query)
    filtered = []

    for product in products:
        if intents["category"] and product["category"].lower() != intents["category"].lower():
            continue

        if intents["max_price"] and product["price"] > intents["max_price"]:
            continue
        if intents["min_price"] and product["price"] < intents["min_price"]:
            continue

        score = 0
        reasons = []

        if intents["budget"] and intents["budget"] in product["tags"]:
            score += 3
            reasons.append("matches budget tier")
        elif intents["budget"] == "premium" and "premium" in product["tags"]:
            score += 3
            reasons.append("matches premium tier")

        if intents["use_case"] and intents["use_case"] in product["tags"]:
            score += 4
            reasons.append(f"strong for {intents['use_case']}")

        if intents["use_case"] == "camera" and product["category"] == "Phone":
            score += 2
        if intents["use_case"] == "gaming" and product["category"] == "TV":
            score += 2
        if intents["use_case"] == "coding" and product["category"] == "Laptop":
            score += 2

        if "budget" in product["tags"] and intents["budget"] == "budget":
            score += 1

        if product["price"] <= 400:
            score += 1

        filtered.append({
            "id": product["id"],
            "name": product["name"],
            "brand": product["brand"],
            "category": product["category"],
            "price": product["price"],
            "score": score,
            "reason": ", ".join(reasons) or "Good catalog match",
        })

    filtered.sort(key=lambda item: (-item["score"], item["price"]))
    return filtered[:5]


@app.route('/')
def index():
    return render_template('ecommerce_search.html')


@app.route('/api/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"products": [], "message": "Please enter a product search request."})

    intents = extract_intents(query)
    products_found = rank_products(query)

    summary_parts = []
    if intents['category']:
        summary_parts.append(f"Category: {intents['category']}")
    if intents['max_price']:
        summary_parts.append(f"Budget cap: ${intents['max_price']}")
    if intents['use_case']:
        summary_parts.append(f"Use case: {intents['use_case']}")
    if not summary_parts:
        summary_parts.append("Open-ended product discovery")

    return jsonify({
        "products": products_found,
        "agent_summary": "Parsed intent: " + "; ".join(summary_parts),
        "message": f"Found {len(products_found)} relevant products for your request."
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
