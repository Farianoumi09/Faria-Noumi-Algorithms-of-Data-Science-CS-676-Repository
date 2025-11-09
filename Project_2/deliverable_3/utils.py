import random
import logging
import os

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(filename="logs/app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# References database
topic_references = {
    "climate change": [
        "https://climate.nasa.gov/",
        "https://www.ipcc.ch/reports/",
        "https://www.un.org/en/climatechange"
    ],
    "ai ethics": [
        "https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai",
        "https://www.oecd.org/going-digital/ai/principles/"
    ],
    "future technology": [
        "https://www.technologyreview.com/",
        "https://www.weforum.org/focus/future-of-technology"
    ]
}

def validate_persona(persona):
    valid_skills = ["Low", "Medium", "High"]
    valid_behaviors = ["Analytical", "Curious", "Exploratory", "Decisive"]
    if persona['technical_skill'] not in valid_skills:
        raise ValueError(f"Invalid technical_skill: {persona['technical_skill']}")
    if persona['behavior_pattern'] not in valid_behaviors:
        raise ValueError(f"Invalid behavior_pattern: {persona['behavior_pattern']}")

def generate_conversation(persona, topic):
    try:
        validate_persona(persona)
        name = persona['name']
        occupation = persona['occupation']
        behavior = persona['behavior_pattern']

        greetings = [
            f"Hi, I'm {name}. As a {occupation}, let's discuss {topic}.",
            f"{name} here! I have some thoughts on {topic}.",
            f"Hello! I've been thinking about {topic}, let me share my perspective."
        ]
        response = random.choice(greetings) + "\n\n"

        # Cause & effect
        causes_effects = {
            "climate change": (["carbon emissions", "deforestation", "overconsumption"], ["temperature rise", "extreme weather", "biodiversity loss"]),
            "ai ethics": (["bias", "privacy issues", "lack of transparency"], ["unfair decisions", "privacy violations", "societal distrust"]),
            "future technology": (["rapid automation", "AI innovation", "renewable tech"], ["job shifts", "efficiency gains", "environmental improvements"])
        }
        topic_lower = topic.lower()
        if topic_lower in causes_effects:
            causes, effects = causes_effects[topic_lower]
            response += "- Causes: " + ", ".join(random.sample(causes, min(3, len(causes)))) + ".\n"
            response += "- Effects: " + ", ".join(random.sample(effects, min(3, len(effects)))) + ".\n"

        # Opinion
        behavior_opinion = {
            "Analytical": ["I like to analyze data and find measurable solutions.", "I prefer evidence-based strategies."],
            "Curious": ["I enjoy exploring innovative approaches.", "I love learning and testing new ideas."],
            "Exploratory": ["I encourage experimentation and creative awareness-raising.", "I explore multiple perspectives."],
            "Decisive": ["I focus on concrete actions and policies.", "I prefer strategies that produce real impact."]
        }
        response += "- Opinion: " + random.choice(behavior_opinion.get(behavior, ["I have thoughtful insights."])) + "\n"

        # Future thoughts
        future_high = ["I support sustainable technology and proactive policies.", "I advocate for long-term innovation."]
        future_low = ["Small lifestyle changes and awareness help.", "Community actions are very important."]
        if persona['technical_skill'] in ["High", "Medium"]:
            response += "- Future thoughts: " + random.choice(future_high) + "\n"
        else:
            response += "- Future thoughts: " + random.choice(future_low) + "\n"

        # References
        if topic_lower in topic_references:
            refs = topic_references[topic_lower]
            response += "- References:\n"
            for ref in refs:
                response += f"  • {ref}\n"

        closings = ["That's my take! Hope it helps.", "What are your thoughts?", "I hope this perspective is useful."]
        response += "\n" + random.choice(closings)

        logging.info(f"Generated conversation for {name} on topic: {topic}")
        return response

    except Exception as e:
        logging.error(f"Error generating conversation for {persona['name']}: {str(e)}")
        return f"Sorry, an error occurred for {persona['name']}."
