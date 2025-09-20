# --- Deliverable 1: Percentage + JSON Output (Spec-Compliant) ---

from urllib.parse import urlparse

def evaluate_source_credibility(url: str) -> dict:
    """
    Credibility scoring function.
    Returns:
      - score (float, 0–1) for machine use
      - score_percentage (0–100%) for human readability
      - explanation (string)
    """

    # Basic validation
    if not isinstance(url, str) or not url.strip():
        return {
            "score": 0.0,
            "score_percentage": 0,
            "explanation": "Invalid input: URL is empty or not a string."
        }

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return {
            "score": 0.0,
            "score_percentage": 0,
            "explanation": "Invalid URL format."
        }

    domain = parsed.netloc.lower()

    # Credibility rules
    score = 50  # Neutral baseline (percentage)
    explanation_parts = []

    # Rule 1: Domain type
    if domain.endswith((".edu", ".gov", ".org")):
        score += 30
        explanation_parts.append("Trusted domain (.edu, .gov, .org).")
    elif domain.endswith((".blogspot.com", ".wordpress.com", ".substack.com")):
        score -= 20
        explanation_parts.append("Blogging/free publishing platform (less reliable).")
    else:
        explanation_parts.append("General/commercial domain, neutral credibility.")

    # Rule 2: HTTPS check
    if parsed.scheme == "https":
        score += 10
        explanation_parts.append("Secure HTTPS connection detected.")
    else:
        score -= 10
        explanation_parts.append("Non-secure HTTP detected.")

    # Normalize percentage
    score = max(0, min(100, score))

    # Convert percentage → decimal (0–1 scale, 2 decimal places)
    score_decimal = round(score / 100, 2)

    # Join explanation
    explanation = " ".join(explanation_parts)

    return {
        "score": score_decimal,          # machine-friendly
        "score_percentage": score,       # human-friendly
        "explanation": explanation       # reasoning
    }


# --- Test Cases ---
test_urls = [
    "https://www.nih.gov/health-information",
    "http://randomblog.blogspot.com/post",
    "https://example.com/news",
    "bad-url"
]

for url in test_urls:
    print(url, "->", evaluate_source_credibility(url))
