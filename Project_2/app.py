import streamlit as st
from textblob import TextBlob
from datetime import datetime
import os
import random

# -------------------------------
# Mock Persona & Troupe classes
# -------------------------------
class Persona:
    def __init__(self, name, traits, age, profession):
        self.name = name
        self.traits = traits
        self.age = age
        self.profession = profession

class Troupe:
    def __init__(self, personas):
        self.personas = personas

    def simulate(self, prompt):
        # Generate a fake response for each persona
        conversation = {}
        for persona in self.personas:
            # Mock response: combine traits, profession, prompt
            response = f"{persona.name} ({', '.join(persona.traits)}, {persona.profession}) responds to '{prompt}' with thoughtful insights."
            # Randomly add humor or empathy based on traits
            if "humorous" in persona.traits:
                response += " Haha, that's interesting!"
            if "empathetic" in persona.traits:
                response += " I can totally relate to that."
            conversation[persona.name] = response
        return conversation

# -------------------------------
# Streamlit App
# -------------------------------
st.title("Mock TinyTroupe Persona Simulator")
st.write("Simulate multiple AI personas (mock version), evaluate responses, and save conversation history.")

# Create folder for conversation logs
if not os.path.exists("conversation_history"):
    os.makedirs("conversation_history")

# User inputs
user_prompt = st.text_area("Enter your prompt:", "Discuss renewable energy technologies.")
turns = st.slider("Number of conversation turns:", 1, 5, 2)

persona_options = st.multiselect(
    "Select personas to include:",
    ["Alex (Analytical Engineer)", "Maria (Friendly Teacher)", "Jordan (Humorous Artist)"],
    default=["Alex (Analytical Engineer)", "Maria (Friendly Teacher)"]
)

# Define personas
persona_dict = {
    "Alex (Analytical Engineer)": Persona(name="Alex", traits=["curious", "analytical"], age=30, profession="engineer"),
    "Maria (Friendly Teacher)": Persona(name="Maria", traits=["friendly", "empathetic"], age=25, profession="teacher"),
    "Jordan (Humorous Artist)": Persona(name="Jordan", traits=["humorous", "creative"], age=28, profession="artist")
}

selected_personas = [persona_dict[name] for name in persona_options]
troupe = Troupe(selected_personas)

# Evaluate response
def evaluate_response(text):
    sentiment = TextBlob(text).sentiment.polarity
    length_score = min(len(text.split()) / 50, 1.0)
    sentiment_score = (sentiment + 1) / 2
    return round((length_score * 0.5 + sentiment_score * 0.5) * 100, 2)

# Run simulation
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
    
    # Save conversation history
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_filename = f"conversation_history/conversation_{timestamp}.md"
    
    with open(md_filename, "w") as f:
        f.write(f"# Conversation History - {timestamp}\n\n")
        for entry in conversation_log:
            f.write(f"### Turn {entry['turn']} - {entry['persona']}\n")
            f.write(f"**Prompt:** {entry['prompt']}\n\n")
            f.write(f"**Response:** {entry['response']}\n\n")
            f.write(f"**Score:** {entry['score']}/100\n\n")
    
    st.success(f"Conversation saved to `{md_filename}`")
