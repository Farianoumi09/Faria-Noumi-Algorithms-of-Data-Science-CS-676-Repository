# === project1/app.py ===
# Author: Faria Noumi
# Date: October 12, 2025
# Description: Advanced Credibility Scoring App for Chatbot
# ----------------------------------------------------------
# This app estimates the credibility of a given text input using
# a mix of heuristic (keyword-based) scoring and random variation.
# It is designed for demonstration and can easily be replaced
# with a fine-tuned Hugging Face transformer model later.

import time
import random
import gradio as gr

# --- Optional: Uncomment when a trained model is available ---
# from transformers import pipeline
# model = pipeline("text-classification", model="your-username/credibility-model")


# --- Helper function for explanation ---
def explain_score(text, score):
    explanations = []

    credible_terms = ["research", "evidence", "study", "verified", "source", "report"]
    unreliable_terms = ["rumor", "believe", "heard", "guess", "fake", "conspiracy"]

    if any(word in text.lower() for word in credible_terms):
        explanations.append("Contains credible keywords like 'research' or 'evidence'.")
    if any(word in text.lower() for word in unreliable_terms):
        explanations.append("Includes unreliable words like 'rumor' or 'fake'.")
    if len(text.split()) < 5:
        explanations.append("Text is too short to evaluate confidently.")
    if score > 0.85:
        explanations.append("Language structure and tone appear formal and factual.")
    elif score < 0.65:
        explanations.append("Tone suggests uncertainty or speculation.")

    if not explanations:
        explanations.append("No strong credibility indicators detected.")
    return "• " + "\n• ".join(explanations)


# --- Core Function ---
def calculate_credibility_score(text):
    """
    Calculates a credibility score for a given text.
    Uses mock logic for demonstration purposes.
    """

    if not text.strip():
        return {"Error": "Please enter some text."}

    # Simulate model processing delay
    time.sleep(random.uniform(0.3, 1.0))

    # Mock logic: keyword-based boost
    base_score = 0.5
    credible_words = ["research", "verified", "confirmed", "study", "report", "data"]
    unreliable_words = ["rumor", "fake", "untrue", "believe", "guess", "hearsay"]

    for word in credible_words:
        if word in text.lower():
            base_score += 0.05
    for word in unreliable_words:
        if word in text.lower():
            base_score -= 0.05

    # Add random variation
    score = max(0.0, min(base_score + random.uniform(-0.1, 0.2), 1.0))

    # Determine rating
    if score >= 0.8:
        rating = "High Credibility ✅"
    elif score >= 0.6:
        rating = "Moderate Credibility ⚠️"
    else:
        rating = "Low Credibility ❌"

    # Explanation
    explanation = explain_score(text, score)

    # --- Uncomment for real model integration ---
    # result = model(text)
    # score = result[0]['score']
    # rating = result[0]['label']

    result_text = (
        f"🔹 **Input:** {text}\n\n"
        f"🔸 **Credibility Score:** {round(score, 3)}\n"
        f"🔸 **Rating:** {rating}\n\n"
        f"### Explanation\n{explanation}"
    )

    return result_text


# --- Gradio Interface (using Blocks for better design) ---
with gr.Blocks(title="Chatbot Credibility Scoring App") as demo:
    gr.Markdown(
        """
        # 🤖 Chatbot Credibility Scoring App  
        Evaluate how trustworthy or credible a piece of text appears to be.
        The score is estimated based on language cues and mock reasoning logic.  
        *(Future versions will connect to a real Hugging Face model.)*
        """
    )

    with gr.Row():
        input_box = gr.Textbox(
            label="Enter text to analyze",
            lines=5,
            placeholder="Example: 'Recent research confirms that vaccines are effective.'",
        )

    with gr.Row():
        output_box = gr.Markdown(label="Credibility Analysis")

    with gr.Row():
        analyze_btn = gr.Button("Analyze Credibility")

    analyze_btn.click(
        fn=calculate_credibility_score,
        inputs=input_box,
        outputs=output_box,
    )

    gr.Markdown("---")
    gr.Markdown(
        "Developed by **Faria Noumi** · Project 1 · October 2025"
    )


# --- Launch App ---
if __name__ == "__main__":
    demo.launch()
