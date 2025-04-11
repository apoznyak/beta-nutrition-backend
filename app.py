
from flask import Flask, request, jsonify

app = Flask(__name__)

FOOD_CATEGORIES = {
    "sugary cereal": ("cariogenic", "High sugar content, sticky texture"),
    "orange juice": ("cariogenic", "Acidic and high in sugar"),
    "chips": ("cariogenic", "Starch sticks to teeth and feeds bacteria"),
    "cheese": ("protective", "Buffers acid and stimulates saliva"),
    "milk": ("protective", "Contains calcium and helps remineralize enamel"),
    "apple": ("neutral", "Contains natural sugar but also fiber and water"),
    "grilled chicken": ("neutral", "Low in sugar and not acidic")
}

@app.route("/calculate-risk", methods=["POST"])
def calculate_risk():
    data = request.get_json()
    food_input = data.get("foodInput", "").lower()

    items = [item.strip() for item in food_input.replace("Breakfast:", "")
                                                 .replace("Lunch:", "")
                                                 .replace("Dinner:", "")
                                                 .replace("Snacks:", "")
                                                 .replace("Drinks:", "").split(",")]

    breakdown = []
    risk_score = 0

    for item in items:
        item = item.strip()
        if item in FOOD_CATEGORIES:
            category, reason = FOOD_CATEGORIES[item]
            breakdown.append({"item": item, "category": category, "reason": reason})
            if category == "cariogenic":
                risk_score += 2
            elif category == "protective":
                risk_score -= 1

    risk_score = max(0, min(10, round(risk_score + 5, 1)))

    if risk_score >= 8:
        risk_level = "High"
    elif risk_score >= 5:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return jsonify({
        "score": risk_score,
        "riskLevel": risk_level,
        "explanation": "Based on the balance of cariogenic and protective foods.",
        "breakdown": breakdown
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
