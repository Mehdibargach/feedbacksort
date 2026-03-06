"""
FeedbackSort — Dashboard synthesis module.
Computes distributions, top problems, and summary metrics from classifications.
"""

from collections import Counter


def compute_dashboard(classifications: list[dict]) -> dict:
    """Compute dashboard metrics from classification results.

    Args:
        classifications: list of dicts with sentiment, category, priority

    Returns:
        dict with distributions, top_problems, and summary
    """
    total = len(classifications)
    if total == 0:
        return {"error": "No classifications to analyze"}

    # Distributions
    sentiments = Counter(c["sentiment"] for c in classifications)
    categories = Counter(c["category"] for c in classifications)
    priorities = Counter(c["priority"] for c in classifications)

    # Top 5 problems: negative reviews grouped by (category, priority)
    negative_reviews = [c for c in classifications if c["sentiment"] == "Negative"]
    problem_combos = Counter(
        (c["category"], c["priority"]) for c in negative_reviews
    )
    top_problems = [
        {
            "category": cat,
            "priority": pri,
            "count": count,
            "percentage": round(count / total * 100, 1),
        }
        for (cat, pri), count in problem_combos.most_common(5)
    ]

    # Summary metrics
    negative_count = sentiments.get("Negative", 0)
    critical_count = priorities.get("Critical", 0)
    top_category = categories.most_common(1)[0] if categories else ("N/A", 0)

    summary = {
        "total_reviews": total,
        "negative_percentage": round(negative_count / total * 100, 1),
        "critical_count": critical_count,
        "top_category": top_category[0],
        "top_category_count": top_category[1],
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
