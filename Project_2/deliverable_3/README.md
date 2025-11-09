---
title: "Smart AI Feedback Simulator"
colorFrom: purple
colorTo: indigo
sdk: streamlit
sdk_version: "1.28.0"
app_file: app.py
pinned: false
---

# Smart AI Feedback Simulator

## Overview  
Interactive app simulating AI‑driven persona conversations on **any topic**, enabling cause/effect reasoning, future thoughts, persona‑specific opinions, and references to credible sources.

## Features  
- Multi‑persona selection from a diverse profile set  
- Enter **any topic** (e.g., climate change, AI ethics, future tech)  
- Generate realistic persona dialogues with:  
  - Dynamic cause & effect insights  
  - Future outlook and recommendations  
  - Credible references/sources  
- Robust production‑ready architecture:  
  - Logging and error handling  
  - Expandable persona database  
  - Ready for cloud deployment via Hugging Face Spaces  

## Running Locally  
```bash
git clone https://huggingface.co/spaces/FariaNoumi09/Project_2_Deliverable_3
cd Project_2_Deliverable_3
pip install -r requirements.txt
streamlit run app.py
