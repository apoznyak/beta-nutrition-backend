# AI-Powered Caries Risk Calculator Backend (Flask)

from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np
import re

app = Flask(__name__)

# Dummy training data (you'll expand this with real samples)
training_data = [
    ("soda chips candy", "High"),
    ("cheese apple water", "Low"),
    ("bread juice cookies", "Moderate"),
    ("milk nuts carrots", "Low"),
    ("smoothie crackers", "Moderate"),
    ("ice cream chocolate cake", "High")
]

texts, labels = zip(*training_data)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(texts)

label_map = {"Low": 0, "Moderate": 1, "High": 2}
y_train = [label_map[label] for label in labels]

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

@app.route("/calculate-risk", methods=["POST"])
def calculate_risk():
    data = request.get_json()
    food_input = data.get("foodInput", "").lower()
    clean_input = re.sub(r"[^a-zA-Z\s]", "", food_input)
    X_input = vectorizer.transform([clean_input])
    pred = model.predict(X_input)[0]
    score = float(model.predict_proba(X_input).max())

    reverse_map = {0: "Low", 1: "Moderate", 2: "High"}
    explanation = {
        "High": "Your input included several high-sugar or sticky items associated with caries risk.",
        "Moderate": "Some processed or sugary foods detected. Consider reducing frequency.",
        "Low": "Your input reflects mostly protective or low-risk items. Keep it up!"
    }

    return jsonify({
        "riskLevel": reverse_map[pred],
        "score": round(score * 10, 2),
        "explanation": explanation[reverse_map[pred]]
    })

if __name__ == "__main__":
    app.run(debug=True)
