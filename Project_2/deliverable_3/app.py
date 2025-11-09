import streamlit as st
import pandas as pd
from utils import generate_conversation
import logging

st.set_page_config(page_title="Smart AI Feedback Simulator", layout="wide")
st.title("🤖 Smart AI Feedback Simulator")

# Load personas
try:
    personas = pd.read_csv("personas.csv")
except Exception as e:
    st.error("Failed to load persona database.")
    logging.error(f"Error loading personas.csv: {str(e)}")
    st.stop()

# User selection
selected_personas = st.multiselect("Select Persona(s):", personas['name'])
topic = st.text_input("Enter any topic (e.g., climate change, AI ethics, future tech):")

if st.button("Start Conversation"):
    if not selected_personas or topic.strip() == "":
        st.warning("Please select at least one persona and enter a topic!")
    else:
        for persona_name in selected_personas:
            persona = personas[personas['name'] == persona_name].iloc[0]
            conversation = generate_conversation(persona, topic)
            st.subheader(f"Conversation with {persona_name}")
            st.write(conversation)
