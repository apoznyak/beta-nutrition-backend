# AI-Powered Caries Risk Calculator with Severity Score
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Food scoring dictionary: values increase/decrease risk
risk_values = {
    "soda": 3, "juice": 2, "cake": 3, "candy": 3, "chips": 2, "cookies": 2, "ice cream": 3, "chocolate": 2,
    "bread": 1, "crackers": 1, "muffin": 2, "smoothie": 2,
    "apple": -1, "carrot": -1, "celery": -1, "cucumber": -1, "banana": 0,
    "milk": -2, "cheese": -2, "nuts": -1, "yogurt": -1, "water": -3
}

@app.route("/calculate-risk", methods=["POST"])
def calculate_risk():
    data = request.get_json()
    food_input = data.get("foodInput", "").lower()
    words = re.findall(r"\b\w+\b", food_input)

    score = 0
    for word in words:
        score += risk_values.get(word, 0)

    score = min(max(score, 0), 10)  # Normalize between 0 and 10

    if score >= 8:
        risk = "High Risk"
    elif score >= 5:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"

    explanation = f"Based on the foods you entered, your risk score is {score}. This reflects the balance between cariogenic and protective foods."

    return jsonify({
        "score": round(score, 2),
        "riskLevel": risk,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)
