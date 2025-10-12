# === project 1/app.py ===
# Author: Faria Noumi
# Date: October 12, 2025
# Description: Credibility scoring app for chatbot

import time
import random
import gradio as gr

# --- Uncomment this section if you have a real Hugging Face model ---
# from transformers import pipeline
# model = pipeline("text-classification", model="your-username/credibility-model")

def calculate_credibility_score(text):
    """
    Returns a credibility score for the input text.
    Replace mock logic with real Hugging Face model if available.
    """
    if not text.strip():
        return "Error: No input text provided"

    # --- Mock scoring logic ---
    time.sleep(random.uniform(0.2, 1.0))
    score = random.uniform(0.6, 0.95)
    rating = "High" if score > 0.75 else "Moderate"

    # --- Uncomment below to use real Hugging Face model ---
    # result = model(text)
    # score = result[0]['score']
    # rating = result[0]['label']

    return f"Input: {text}\nCredibility Score: {round(score,3)}\nRating: {rating}"

# --- Gradio Interface ---
iface = gr.Interface(
    fn=calculate_credibility_score,
    inputs=gr.Textbox(lines=3, placeholder="Enter text to check credibility..."),
    outputs=gr.Textbox(label="Credibility Result"),
    title="Chatbot Credibility Scoring",
    description="Enter text to get a credibility score."
)

# --- Launch App ---
iface.launch()
