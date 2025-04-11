# AI-Powered Caries Risk Calculator with Severity Score (Updated Keywords)

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Improved scoring dictionary with common junk/protective foods
risk_values = {
    # High risk foods (3 points)
    "cake": 3, "candy": 3, "soda": 3, "ice cream": 3, "chocolate": 3,
    # Moderate risk foods (2 points)
    "cookies": 2, "chips": 2, "muffin": 2, "juice": 2, "smoothie": 2,
    # Slight risk (1 point)
    "crackers": 1, "bread": 1, "cereal": 1,
    # Neutral (0 points)
    "banana": 0, "fruit": 0,
    # Protective foods (-1 to -3)
    "apple": -1, "carrot": -1, "celery": -1, "cucumber": -1,
    "milk": -2, "cheese": -2, "yogurt": -2, "nuts": -2, "water": -3
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