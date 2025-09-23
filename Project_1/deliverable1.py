# --- Deliverable 1: Percentage + JSON Output (Spec-Compliant) ---

import re
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from urllib.parse import urlparse
import json

# --- Configuration ---
FEATURE_WEIGHTS = {
    "author_presence": 0.15,
    "domain_credibility": 0.25,
    "citations": 0.20,
    "text_objectivity": 0.25,
    "sentiment_neutrality": 0.15
}

RULES = {
    "trusted_domains": [
        'cdc.gov', 'who.int', 'nih.gov', 'fda.gov', 'mayoclinic.org', 
        'jamanetwork.com', 'nejm.org', 'health.harvard.edu', 'webmd.com'
    ],
    "untrusted_domains": [
        'naturalnews.com', 'mercola.com', 'healthimpactnews.com', 'thehealthyhomeeconomist.com'
    ]
}

# --- Utility: Fetch article text ---
def fetch_text(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for s in soup(['script', 'style']):
            s.decompose()
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
        return ' '.join(paragraphs)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# --- Feature Extraction ---
def extract_features(text, url=None):
    features = {}
    
    # Author presence
    features["author_presence"] = 1 if re.search(r'\b(by|author|doctor|md|phd)\b', text[:500], re.IGNORECASE) else 0
    
    # Citations
    features["citations"] = 1 if re.search(r'\b(sources|references|citations|bibliography|study|journal)\b', text, re.IGNORECASE) else 0
    
    # Domain credibility
    if url:
        domain = urlparse(url).netloc.lower().replace('www.', '')
        if any(domain.endswith(d) for d in RULES["trusted_domains"]):
            features["domain_credibility"] = 1
        elif any(domain.endswith(d) for d in RULES["untrusted_domains"]):
            features["domain_credibility"] = 0
        else:
            features["domain_credibility"] = 0.5
    else:
        features["domain_credibility"] = 0.5
    
    # Text objectivity
    blob = TextBlob(text)
    subj_score = 1 - blob.sentiment.subjectivity
    features["text_objectivity"] = subj_score
    
    # Sentiment neutrality
    features["sentiment_neutrality"] = 1 - abs(blob.sentiment.polarity)
    
    return features

# --- ML-Based Scoring (Simulated) ---
def ml_score(features):
    score = 0
    explanations = []
    for f, weight in FEATURE_WEIGHTS.items():
        contribution = features[f] * weight * 100
        score += contribution
        explanations.append(f"[{contribution:.1f}] Feature '{f}' contribution")
    return max(0, min(100, score)), explanations

# --- Rule-Based Sanity Checks ---
def rule_based_adjustments(text, url=None):
    score_adjustment = 0
    explanations = []
    
    # Penalize sensational language
    num_caps = len(re.findall(r'\b[A-Z]{4,}\b', text))
    num_excl = text.count('!')
    if num_caps > 5 or num_excl > 5:
        penalty = min((num_caps + num_excl - 10) * 2, 20)
        score_adjustment -= penalty
        explanations.append(f"[-{penalty}] Sensational language detected (avoid panic-inducing terms).")
    else:
        explanations.append("[+/- 0] Language is calm and neutral.")
    
    return score_adjustment, explanations

# --- Hybrid Analyzer ---
def analyze_credibility(input_data, return_json=False):
    text, url = input_data, None
    if input_data.startswith(('http://', 'https://')):
        url = input_data
        text = fetch_text(url)
        if not text:
            print("Failed to fetch content from URL.")
            return
    if len(text) < 100:
        print("Text too short for meaningful analysis.")
        return
    
    # Extract features
    features = extract_features(text, url)
    
    # ML-Based Score
    ml_final_score, ml_explanations = ml_score(features)
    
    # Rule-Based Adjustments
    rule_adjustment, rule_explanations = rule_based_adjustments(text, url)
    
    # Combine scores
    final_score = ml_final_score + rule_adjustment
    final_score = max(0, min(100, final_score))
    
    # --- Output ---
    if return_json:
        return json.dumps({
            "final_score": round(final_score,2),
            "ml_score": round(ml_final_score,2),
            "rule_adjustment": round(rule_adjustment,2),
            "ml_explanations": ml_explanations,
            "rule_explanations": rule_explanations,
            "features": features,
            "url": url
        }, indent=2)
    
    # Print report
    print("\n" + "="*60)
    print("          PUBLIC HEALTH CREDIBILITY ANALYSIS")
    print("="*60)
    print(f"FINAL SCORE: {final_score:.2f}/100\n")
    
    print("ML-Based Feature Contributions:")
    for e in ml_explanations:
        print(f"  - {e}")
    
    print("\nRule-Based Adjustments:")
    for e in rule_explanations:
        print(f"  - {e}")
    
    print("\nExtracted Features:")
    for k,v in features.items():
        print(f"  - {k}: {v}")
    
    print("="*60)

# --- Run Analyzer ---
if __name__ == "__main__":
    user_input = input("Enter a public health article URL or paste text:\n> ").strip()
    if user_input:
        analyze_credibility(user_input)
