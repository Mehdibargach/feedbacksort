"""
FeedbackSort — Walking Skeleton Test
Tests WS-1 through WS-7 against the 10-review test CSV.
"""

import pandas as pd
import time
from classifier import detect_text_column, classify_reviews, VALID_SENTIMENTS, VALID_CATEGORIES, VALID_PRIORITIES


def run_ws_tests():
    print("=" * 60)
    print("FeedbackSort — Walking Skeleton Tests")
    print("=" * 60)

    # Load test data
    df = pd.read_csv("data/ws-test-reviews.csv")
    print(f"\nLoaded {len(df)} reviews from ws-test-reviews.csv")
    print(f"Columns: {list(df.columns)}")

    # WS-1: CSV parsing + auto-detection
    print("\n--- WS-1: CSV parsing + auto-detection ---")
    text_col = detect_text_column(df)
    ws1_pass = text_col == "review_text" and len(df.columns) > 3
    print(f"Detected text column: '{text_col}'")
    print(f"Number of columns: {len(df.columns)}")
    print(f"WS-1: {'PASS' if ws1_pass else 'FAIL'}")

    # Run classification
    print("\n--- Classifying 10 reviews... ---")
    reviews = [{"id": row["id"], "text": row["review_text"]} for _, row in df.iterrows()]
    start = time.time()
    results = classify_reviews(reviews)
    elapsed = time.time() - start
    print(f"Classification done in {elapsed:.2f}s")
    print(f"Got {len(results)} results")

    # Build lookup
    result_map = {r["review_id"]: r for r in results}

    # WS-2: Format output valide
    print("\n--- WS-2: Format output valide ---")
    ws2_pass = True
    for r in results:
        if r["sentiment"] not in VALID_SENTIMENTS:
            print(f"  INVALID sentiment: {r['sentiment']} (review {r['review_id']})")
            ws2_pass = False
        if r["category"] not in VALID_CATEGORIES:
            print(f"  INVALID category: {r['category']} (review {r['review_id']})")
            ws2_pass = False
        if r["priority"] not in VALID_PRIORITIES:
            print(f"  INVALID priority: {r['priority']} (review {r['review_id']})")
            ws2_pass = False
    if len(results) != 10:
        print(f"  Expected 10 results, got {len(results)}")
        ws2_pass = False
    print(f"WS-2: {'PASS' if ws2_pass else 'FAIL'}")

    # WS-3, WS-4, WS-5: Precision
    print("\n--- WS-3/4/5: Precision ---")
    sentiment_correct = 0
    category_correct = 0
    priority_correct = 0

    print(f"\n{'ID':>3} | {'Expected Sent':>14} | {'Got Sent':>14} | {'Expected Cat':>18} | {'Got Cat':>18} | {'Expected Pri':>12} | {'Got Pri':>12}")
    print("-" * 110)

    for _, row in df.iterrows():
        rid = row["id"]
        r = result_map.get(rid, {})

        exp_s = row["expected_sentiment"]
        got_s = r.get("sentiment", "MISSING")
        exp_c = row["expected_category"]
        got_c = r.get("category", "MISSING")
        exp_p = row["expected_priority"]
        got_p = r.get("priority", "MISSING")

        s_ok = "✓" if exp_s == got_s else "✗"
        c_ok = "✓" if exp_c == got_c else "✗"
        p_ok = "✓" if exp_p == got_p else "✗"

        if exp_s == got_s:
            sentiment_correct += 1
        if exp_c == got_c:
            category_correct += 1
        if exp_p == got_p:
            priority_correct += 1

        print(f"{rid:>3} | {exp_s:>14} | {got_s:>14} {s_ok} | {exp_c:>18} | {got_c:>18} {c_ok} | {exp_p:>12} | {got_p:>12} {p_ok}")

    print(f"\nSentiment: {sentiment_correct}/10 ({sentiment_correct*10}%)")
    print(f"Category:  {category_correct}/10 ({category_correct*10}%)")
    print(f"Priority:  {priority_correct}/10 ({priority_correct*10}%)")

    ws3_pass = sentiment_correct >= 9
    ws4_pass = category_correct >= 8
    ws5_pass = priority_correct >= 7

    print(f"\nWS-3 (sentiment >= 9/10): {'PASS' if ws3_pass else 'FAIL'} ({sentiment_correct}/10)")
    print(f"WS-4 (category >= 8/10):  {'PASS' if ws4_pass else 'FAIL'} ({category_correct}/10)")
    print(f"WS-5 (priority >= 7/10):  {'PASS' if ws5_pass else 'FAIL'} ({priority_correct}/10)")

    # WS-6: Adversarial sarcasm (review 4)
    print("\n--- WS-6: Adversarial sarcasm ---")
    r4 = result_map.get(4, {})
    ws6_pass = r4.get("sentiment") == "Negative"
    print(f"Review 4: 'Great, another crash. Love it.'")
    print(f"Expected: Negative | Got: {r4.get('sentiment', 'MISSING')}")
    print(f"WS-6: {'PASS' if ws6_pass else 'FAIL'}")

    # WS-7: Adversarial ambiguous (review 3)
    print("\n--- WS-7: Adversarial ambiguous ---")
    r3 = result_map.get(3, {})
    ws7_pass = r3.get("sentiment") == "Neutral"
    print(f"Review 3: \"It's OK I guess. Nothing special but it works.\"")
    print(f"Expected: Neutral | Got: {r3.get('sentiment', 'MISSING')}")
    print(f"WS-7: {'PASS' if ws7_pass else 'FAIL'}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_tests = {
        "WS-1 CSV parsing + auto-detection": ws1_pass,
        "WS-2 Format output valide": ws2_pass,
        "WS-3 Precision sentiment >= 9/10": ws3_pass,
        "WS-4 Precision categorie >= 8/10": ws4_pass,
        "WS-5 Precision priorite >= 7/10": ws5_pass,
        "WS-6 Adversarial sarcasme": ws6_pass,
        "WS-7 Adversarial ambigu": ws7_pass,
    }

    for name, passed in all_tests.items():
        print(f"  {'PASS' if passed else 'FAIL'} — {name}")

    total_pass = sum(all_tests.values())
    print(f"\nTotal: {total_pass}/7 PASS")
    print(f"Latency: {elapsed:.2f}s")
    print(f"\nSkeleton Check: {'OUI — continuer' if total_pass == 7 else 'NON — investiguer'}")


if __name__ == "__main__":
    run_ws_tests()
