import streamlit as st
from tinytoupe import Persona, Troupe
from textblob import TextBlob
import os
from datetime import datetime

# --- Title ---
st.title("Project 2: TinyTroupe Persona Simulator")

# --- Conversation folder ---
if not os.path.exists("conversation_history"):
    os.makedirs("conversation_history")

# --- Inputs ---
user_prompt = st.text_area("Enter your prompt:", "Discuss renewable energy technologies.")
turns = st.slider("Number of conversation turns:", 1, 5, 2)

persona_options = st.multiselect(
    "Select personas:",
    ["Alex (Analytical Engineer)", "Maria (Friendly Teacher)", "Jordan (Humorous Artist)"],
    default=["Alex (Analytical Engineer)", "Maria (Friendly Teacher)"]
)

# --- Define personas ---
persona_dict = {
    "Alex (Analytical Engineer)": Persona(name="Alex", traits=["curious", "analytical"], age=30, profession="engineer"),
    "Maria (Friendly Teacher)": Persona(name="Maria", traits=["friendly", "empathetic"], age=25, profession="teacher"),
    "Jordan (Humorous Artist)": Persona(name="Jordan", traits=["humorous", "creative"], age=28, profession="artist")
}
selected_personas = [persona_dict[name] for name in persona_options]
troupe = Troupe(selected_personas)

# --- Evaluate response ---
def evaluate_response(text):
    sentiment = TextBlob(text).sentiment.polarity
    length_score = min(len(text.split()) / 50, 1.0)
    sentiment_score = (sentiment + 1) / 2
    return round((length_score * 0.5 + sentiment_score * 0.5) * 100, 2)

# --- Run Simulation ---
if st.button("Run Simulation"):
    conversation_log = []
    st.write("### Simulation Results:")
    for turn in range(1, turns + 1):
        st.write(f"**Turn {turn}**")
        conversation = troupe.simulate(prompt=user_prompt)
        for persona_name, response in conversation.items():
            score = evaluate_response(response)
            st.subheader(f"{persona_name} Response:")
            st.write(response)
            st.caption(f"Response Quality Score: {score}/100")
            conversation_log.append({
                "turn": turn,
                "persona": persona_name,
                "prompt": user_prompt,
                "response": response,
                "score": score
            })
        st.write("---")

    # --- Save conversation ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_filename = f"conversation_history/conversation_{timestamp}.md"
    with open(md_filename, "w") as f:
        f.write(f"# Conversation History - {timestamp}\n\n")
        for entry in conversation_log:
            f.write(f"### Turn {entry['turn']} - {entry['persona']}\n")
            f.write(f"**Prompt:** {entry['prompt']}\n\n")
            f.write(f"**Response:** {entry['response']}\n\n")
            f.write(f"**Score:** {entry['score']}/100\n\n")
    st.success(f"Conversation history saved to `{md_filename}`")
