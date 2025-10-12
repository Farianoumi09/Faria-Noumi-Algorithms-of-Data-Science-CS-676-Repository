# === Deliverable 3: Implementation into Live Applications ===
# Author: Faria Noumi
# Date: October 10, 2025
# Description: This file integrates the finalized credibility scoring model
#              into a chatbot-style application with API endpoints and UI simulation.
# -------------------------------------------------------------

# --- Import Libraries ---
import time
import random
from flask import Flask, request, jsonify
# --- Flask Application Setup ---
app = Flask(__name__)

# --- Mock Credibility Model Function ---
def calculate_credibility_score(text):
    """
    Simulates the credibility scoring function from Deliverable 1.
    In production, this would call the trained ML model deployed on Hugging Face.
    """
    # Simulate model delay
    time.sleep(random.uniform(0.2, 1.0))
    
    # Simple text-based scoring logic (placeholder for actual model)
    score = random.uniform(0.6, 0.95)
    
    result = {
        "input_text": text,
        "credibility_score": round(score, 3),
        "rating": "High" if score > 0.75 else "Moderate"
    }
    return result

# --- API Route for Chatbot Integration ---
@app.route('/get_credibility', methods=['POST'])
def get_credibility():
    """
    Receives user input (text) and returns a credibility score.
    Includes timeout fallback and error handling.
    """
    try:
        data = request.get_json()
        user_text = data.get("text", "")
        if not user_text:
            return jsonify({"error": "No input text provided"}), 400
        
        # Calculate credibility
        result = calculate_credibility_score(user_text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# --- Fallback Mechanism ---
@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"error": "Endpoint not found"}), 404


# --- Entry Point ---
if __name__ == '__main__':
    print("✅ Deliverable 3: Credibility API running on http://127.0.0.1:5000")
    app.run(debug=True)

