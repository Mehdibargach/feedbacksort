"""
FeedbackSort — Classifier module
Classifies customer reviews into sentiment, category, and priority using GPT-4o-mini.
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VALID_SENTIMENTS = ["Positive", "Negative", "Neutral"]
VALID_CATEGORIES = [
    "Bug / Crash",
    "UX / Design",
    "Performance",
    "Feature Request",
    "Pricing / Billing",
    "Onboarding",
    "Praise",
]
VALID_PRIORITIES = ["Critical", "High", "Medium", "Low"]

SYSTEM_PROMPT = """You are a customer feedback classifier. For each review, you must assign exactly 3 labels:

1. **sentiment**: The emotional tone of the review.
   - "Positive" — the customer is satisfied or happy
   - "Negative" — the customer is unhappy, frustrated, or reporting a problem
   - "Neutral" — no strong emotion, factual statement, or irrelevant content

2. **category**: The main topic of the review. Pick the SINGLE best match:
   - "Bug / Crash" — the app crashes, freezes, has a technical malfunction
   - "UX / Design" — confusing navigation, ugly interface, poor ergonomics
   - "Performance" — slow loading, lag, high resource usage
   - "Feature Request" — user wants a feature that doesn't exist yet
   - "Pricing / Billing" — too expensive, billing issues, subscription complaints
   - "Onboarding" — first-time experience is difficult, no tutorial, hard to get started
   - "Praise" — general compliment, no specific issue raised

3. **priority**: How urgent is this feedback?
   - "Critical" — app is unusable, data loss, security issue, blocking bug
   - "High" — major irritant, frequent issue, impacts core experience
   - "Medium" — moderate friction, improvement desired but not blocking
   - "Low" — nice-to-have, cosmetic, personal preference

IMPORTANT RULES:
- Detect SARCASM. "Great, another crash. Love it." is NEGATIVE, not Positive.
- If the review has no real feedback content (e.g., "First review ever lol"), classify as Neutral / Praise / Low.
- If the review mentions multiple topics, pick the DOMINANT one (the one the user cares about most).
- ONLY use the exact label values listed above. No variations, no synonyms.
- Priority for feature requests with neutral/mild tone ("would be nice", "just a suggestion", "I wonder if") should be LOW, not Medium. Only give Medium to feature requests with strong demand or clear frustration.
- "Critical" requires the app to be UNUSABLE or DATA LOSS. Billing errors (charged twice, wrong charge) are HIGH, not Critical — the app still works.

Respond with a JSON array. Each element must have: review_id, sentiment, category, priority.
"""


def detect_text_column(df):
    """Auto-detect which column contains review text.
    Heuristic: longest average string length among string columns.
    """
    text_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if not text_cols:
        raise ValueError("No text columns found in CSV")
    if len(text_cols) == 1:
        return text_cols[0]
    avg_lengths = {col: df[col].astype(str).str.len().mean() for col in text_cols}
    return max(avg_lengths, key=avg_lengths.get)


def classify_reviews(reviews: list[dict], model: str = "gpt-4o-mini") -> list[dict]:
    """Classify a list of reviews using the LLM.

    Args:
        reviews: list of dicts with at least 'id' and 'text' keys
        model: OpenAI model to use

    Returns:
        list of dicts with review_id, sentiment, category, priority
    """
    user_prompt = "Classify these reviews:\n\n"
    for r in reviews:
        user_prompt += f"[Review {r['id']}]: {r['text']}\n"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = response.choices[0].message.content
    parsed = json.loads(raw)

    # Handle various wrapper keys the LLM might use
    if isinstance(parsed, dict):
        # Try common keys: reviews, results, classifications
        for key in ["reviews", "results", "classifications"]:
            if key in parsed:
                results = parsed[key]
                break
        else:
            # If no known key, take the first list value
            results = next((v for v in parsed.values() if isinstance(v, list)), [])
    else:
        results = parsed

    # Validate each result
    validated = []
    for r in results:
        entry = {
            "review_id": r.get("review_id"),
            "sentiment": r.get("sentiment"),
            "category": r.get("category"),
            "priority": r.get("priority"),
        }
        # Enforce valid values
        if entry["sentiment"] not in VALID_SENTIMENTS:
            entry["sentiment"] = "Neutral"
        if entry["category"] not in VALID_CATEGORIES:
            entry["category"] = "Praise"
        if entry["priority"] not in VALID_PRIORITIES:
            entry["priority"] = "Low"
        validated.append(entry)

    return validated
