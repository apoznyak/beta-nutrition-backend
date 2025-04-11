
from flask import Flask, request, jsonify

app = Flask(__name__)

# Expanded dictionary with lowercase keys and common foods
FOOD_CATEGORIES = {
    "cake": ("cariogenic", "High in sugar and refined flour"),
    "chocolate": ("cariogenic", "High in sugar and sticky texture"),
    "soda": ("cariogenic", "Sugary and acidic drink"),
    "coffee": ("neutral", "Low sugar unless sweetened"),
    "sugary cereal": ("cariogenic", "High sugar content"),
    "orange juice": ("cariogenic", "Acidic and high in sugar"),
    "chips": ("cariogenic", "Starch sticks to teeth and feeds bacteria"),
    "cheese": ("protective", "Buffers acid and stimulates saliva"),
    "milk": ("protective", "Contains calcium and helps remineralize enamel"),
    "apple": ("neutral", "Contains natural sugar but also fiber and water"),
    "grilled chicken": ("neutral", "Low in sugar and not acidic"),
    "bread": ("cariogenic", "Refined starches promote acid production"),
    "cookies": ("cariogenic", "High in sugar and refined flour"),
    "candy": ("cariogenic", "Sticky sugar that clings to teeth"),
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
        else:
            breakdown.append({"item": item, "category": "unknown", "reason": "Not found in food database"})

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
