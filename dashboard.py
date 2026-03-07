"""
FeedbackSort — Dashboard synthesis module.
Computes distributions, top problems with verbatims, and summary metrics.
"""

from collections import Counter, defaultdict


def compute_dashboard(classifications: list[dict], reviews: list[dict] = None) -> dict:
    """Compute dashboard metrics from classification results.

    Args:
        classifications: list of dicts with review_id, sentiment, category, priority
        reviews: optional list of dicts with id and text (for verbatims)

    Returns:
        dict with distributions, top_problems (with sample quotes), and summary
    """
    total = len(classifications)
    if total == 0:
        return {"error": "No classifications to analyze"}

    # Build review text lookup
    text_map = {}
    if reviews:
        text_map = {r["id"]: r["text"] for r in reviews}

    # Distributions
    sentiments = Counter(c["sentiment"] for c in classifications)
    categories = Counter(c["category"] for c in classifications)
    priorities = Counter(c["priority"] for c in classifications)

    # Group negative reviews by (category, priority) with their texts
    negative_by_combo = defaultdict(list)
    for c in classifications:
        if c["sentiment"] == "Negative":
            key = (c["category"], c["priority"])
            negative_by_combo[key].append(c)

    # Top 5 problems with verbatims
    problem_combos = Counter(
        (c["category"], c["priority"])
        for c in classifications
        if c["sentiment"] == "Negative"
    )
    top_problems = []
    for (cat, pri), count in problem_combos.most_common(5):
        # Get up to 3 sample verbatims
        samples = negative_by_combo[(cat, pri)][:3]
        verbatims = []
        for s in samples:
            text = text_map.get(s.get("review_id"), "")
            if text:
                verbatims.append(text)

        top_problems.append({
            "category": cat,
            "priority": pri,
            "count": count,
            "percentage": round(count / total * 100, 1),
            "verbatims": verbatims,
        })

    # Summary — top PROBLEM category (negative only), not top overall
    negative_categories = Counter(
        c["category"] for c in classifications if c["sentiment"] == "Negative"
    )
    top_problem_cat = negative_categories.most_common(1)[0] if negative_categories else ("N/A", 0)

    negative_count = sentiments.get("Negative", 0)
    positive_count = sentiments.get("Positive", 0)
    neutral_count = sentiments.get("Neutral", 0)
    critical_count = priorities.get("Critical", 0)

    summary = {
        "total_reviews": total,
        "negative_count": negative_count,
        "negative_percentage": round(negative_count / total * 100, 1),
        "positive_count": positive_count,
        "positive_percentage": round(positive_count / total * 100, 1),
        "neutral_count": neutral_count,
        "neutral_percentage": round(neutral_count / total * 100, 1),
        "critical_count": critical_count,
        "top_problem_category": top_problem_cat[0],
        "top_problem_category_count": top_problem_cat[1],
    }

    # Format distributions as sorted lists
    def format_dist(counter):
        return [
            {"label": label, "count": count, "percentage": round(count / total * 100, 1)}
            for label, count in counter.most_common()
        ]

    return {
        "distributions": {
            "sentiment": format_dist(sentiments),
            "category": format_dist(categories),
            "priority": format_dist(priorities),
        },
        "top_problems": top_problems,
        "summary": summary,
    }
