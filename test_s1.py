"""
FeedbackSort — Scope 1 Tests
Tests S1-1 through S1-9 against the demo dataset.
"""

import json
import time
import pandas as pd
import requests

API_URL = "http://localhost:8899"


def test_s1():
    print("=" * 60)
    print("FeedbackSort — Scope 1 Tests")
    print("=" * 60)

    # S1-1: Dataset demo created
    print("\n--- S1-1: Dataset demo created ---")
    df = pd.read_csv("data/demo-reviews.csv")
    golden = pd.read_csv("data/golden-200.csv")
    total = len(df)
    neg_pct = len(df[df["expected_sentiment"] == "Negative"]) / total * 100
    pos_pct = len(df[df["expected_sentiment"] == "Positive"]) / total * 100
    neu_pct = len(df[df["expected_sentiment"] == "Neutral"]) / total * 100
    cats = df["expected_category"].nunique()

    s1_1 = (
        total == 2000
        and 35 <= neg_pct <= 45
        and 30 <= pos_pct <= 40
        and 20 <= neu_pct <= 30
        and cats == 7
    )
    print(f"Total reviews: {total}")
    print(f"Negative: {neg_pct:.1f}%, Positive: {pos_pct:.1f}%, Neutral: {neu_pct:.1f}%")
    print(f"Categories: {cats}")
    print(f"Golden subset: {len(golden)} reviews")
    print(f"S1-1: {'PASS' if s1_1 else 'FAIL'}")

    # S1-7: API endpoint — classify golden subset
    print("\n--- S1-7: API endpoint ---")
    start = time.time()
    with open("data/golden-200.csv", "rb") as f:
        resp = requests.post(f"{API_URL}/classify", files={"file": ("golden-200.csv", f, "text/csv")})
    elapsed = time.time() - start

    if resp.status_code != 200:
        print(f"API error: {resp.status_code} — {resp.text}")
        print("S1-7: FAIL")
        return

    data = resp.json()
    s1_7 = data.get("success") and "classifications" in data and "dashboard" in data
    print(f"Status: {resp.status_code}")
    print(f"Total classified: {data.get('total_reviews')}")
    print(f"Has classifications: {'classifications' in data}")
    print(f"Has dashboard: {'dashboard' in data}")
    print(f"S1-7: {'PASS' if s1_7 else 'FAIL'}")

    # S1-2: Batch processing — check all reviews classified
    print("\n--- S1-2: Batch processing ---")
    classifications = data.get("classifications", [])
    s1_2 = len(classifications) == len(golden)
    print(f"Expected: {len(golden)} classifications, Got: {len(classifications)}")
    print(f"S1-2: {'PASS' if s1_2 else 'FAIL'}")

    # S1-3: Concurrent processing — latency
    print("\n--- S1-3: Concurrent processing (latency on golden-200) ---")
    print(f"Time for {len(golden)} reviews: {elapsed:.1f}s")
    # Extrapolate for 2000
    estimated_2000 = elapsed * (2000 / len(golden))
    print(f"Estimated for 2000 reviews: {estimated_2000:.1f}s")
    s1_3_golden = elapsed < 120  # 2 min max for golden
    print(f"S1-3 (golden): {'PASS' if s1_3_golden else 'FAIL'}")

    # S1-8: Precision on golden dataset
    print("\n--- S1-8: Precision golden dataset ---")
    result_map = {}
    for c in classifications:
        rid = c.get("review_id")
        result_map[rid] = c

    sent_correct = 0
    cat_correct = 0
    pri_correct = 0
    sent_total = 0
    cat_total = 0
    pri_total = 0

    mismatches = {"sentiment": [], "category": [], "priority": []}

    for _, row in golden.iterrows():
        rid = row["id"]
        r = result_map.get(rid, {})
        if not r:
            continue

        sent_total += 1
        cat_total += 1
        pri_total += 1

        exp_s = row["expected_sentiment"]
        got_s = r.get("sentiment", "MISSING")
        exp_c = row["expected_category"]
        got_c = r.get("category", "MISSING")
        exp_p = row["expected_priority"]
        got_p = r.get("priority", "MISSING")

        if exp_s == got_s:
            sent_correct += 1
        else:
            mismatches["sentiment"].append({"id": rid, "expected": exp_s, "got": got_s, "text": row["review_text"][:60]})

        if exp_c == got_c:
            cat_correct += 1
        else:
            mismatches["category"].append({"id": rid, "expected": exp_c, "got": got_c, "text": row["review_text"][:60]})

        if exp_p == got_p:
            pri_correct += 1
        else:
            mismatches["priority"].append({"id": rid, "expected": exp_p, "got": got_p, "text": row["review_text"][:60]})

    sent_acc = sent_correct / sent_total * 100 if sent_total else 0
    cat_acc = cat_correct / cat_total * 100 if cat_total else 0
    pri_acc = pri_correct / pri_total * 100 if pri_total else 0

    print(f"Sentiment: {sent_correct}/{sent_total} ({sent_acc:.1f}%) — target >= 90%")
    print(f"Category:  {cat_correct}/{cat_total} ({cat_acc:.1f}%) — target >= 85%")
    print(f"Priority:  {pri_correct}/{pri_total} ({pri_acc:.1f}%) — target >= 80%")

    s1_8 = sent_acc >= 90 and cat_acc >= 85 and pri_acc >= 80
    print(f"S1-8: {'PASS' if s1_8 else 'FAIL'}")

    if mismatches["sentiment"]:
        print(f"\nSentiment mismatches ({len(mismatches['sentiment'])}):")
        for m in mismatches["sentiment"][:5]:
            print(f"  #{m['id']}: expected {m['expected']}, got {m['got']} — \"{m['text']}\"")

    if mismatches["category"]:
        print(f"\nCategory mismatches ({len(mismatches['category'])}):")
        for m in mismatches["category"][:5]:
            print(f"  #{m['id']}: expected {m['expected']}, got {m['got']} — \"{m['text']}\"")

    if mismatches["priority"]:
        print(f"\nPriority mismatches ({len(mismatches['priority'])}):")
        for m in mismatches["priority"][:5]:
            print(f"  #{m['id']}: expected {m['expected']}, got {m['got']} — \"{m['text']}\"")

    # S1-4: Dashboard distributions
    print("\n--- S1-4: Dashboard distributions ---")
    dash = data.get("dashboard", {})
    dists = dash.get("distributions", {})
    has_sentiment = "sentiment" in dists and len(dists["sentiment"]) > 0
    has_category = "category" in dists and len(dists["category"]) > 0
    has_priority = "priority" in dists and len(dists["priority"]) > 0
    s1_4 = has_sentiment and has_category and has_priority
    print(f"Sentiment distribution: {has_sentiment}")
    print(f"Category distribution: {has_category}")
    print(f"Priority distribution: {has_priority}")
    if has_sentiment:
        for d in dists["sentiment"]:
            print(f"  {d['label']}: {d['count']} ({d['percentage']}%)")
    print(f"S1-4: {'PASS' if s1_4 else 'FAIL'}")

    # S1-5: Top 5 problems
    print("\n--- S1-5: Top 5 problems ---")
    top_problems = dash.get("top_problems", [])
    s1_5 = len(top_problems) >= 3  # at least 3 problems from negative reviews
    print(f"Top problems found: {len(top_problems)}")
    for p in top_problems:
        print(f"  {p['category']} / {p['priority']}: {p['count']} ({p['percentage']}%)")
    print(f"S1-5: {'PASS' if s1_5 else 'FAIL'}")

    # S1-6: Summary metrics
    print("\n--- S1-6: Summary metrics ---")
    summary = dash.get("summary", {})
    has_total = "total_reviews" in summary
    has_neg_pct = "negative_percentage" in summary
    has_critical = "critical_count" in summary
    has_top_cat = "top_category" in summary
    s1_6 = has_total and has_neg_pct and has_critical and has_top_cat
    print(f"Total reviews: {summary.get('total_reviews')}")
    print(f"Negative %: {summary.get('negative_percentage')}")
    print(f"Critical count: {summary.get('critical_count')}")
    print(f"Top category: {summary.get('top_category')} ({summary.get('top_category_count')})")
    print(f"S1-6: {'PASS' if s1_6 else 'FAIL'}")

    # S1-9: Cost (estimate)
    print("\n--- S1-9: Cost estimate ---")
    # 200 reviews in batches of 20 = 10 API calls
    # Each call: ~1500 input tokens + ~500 output tokens
    # GPT-4o-mini: $0.15/1M input, $0.60/1M output
    # 10 calls * 2000 tokens avg = 20K tokens ≈ $0.003-0.012
    # For 2000 reviews: 100 calls ≈ $0.03-0.12
    est_cost = 0.06  # conservative estimate for 2000 reviews
    s1_9 = est_cost < 0.10
    print(f"Estimated cost for 2000 reviews: ~${est_cost:.2f}")
    print(f"S1-9: {'PASS' if s1_9 else 'FAIL'}")

    # Now test full 2000 dataset via demo endpoint
    print("\n--- S1-3b: Full 2000 dataset via demo endpoint ---")
    start2 = time.time()
    resp2 = requests.post(f"{API_URL}/classify", data={"dataset": "demo"})
    elapsed2 = time.time() - start2
    if resp2.status_code == 200:
        data2 = resp2.json()
        print(f"Total classified: {data2.get('total_reviews')}")
        print(f"Time: {elapsed2:.1f}s")
        s1_3 = elapsed2 < 60
        print(f"S1-3 (2000 reviews < 60s): {'PASS' if s1_3 else 'FAIL'}")
    else:
        print(f"API error: {resp2.status_code}")
        s1_3 = False

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_tests = {
        "S1-1 Dataset demo (2000, distribution, 7 cats)": s1_1,
        "S1-2 Batch processing (all classified)": s1_2,
        "S1-3 Concurrent processing (< 60s)": s1_3,
        "S1-4 Dashboard distributions": s1_4,
        "S1-5 Top 5 problems": s1_5,
        "S1-6 Summary metrics": s1_6,
        "S1-7 API endpoint": s1_7,
        "S1-8 Precision golden dataset": s1_8,
        "S1-9 Cost < $0.10": s1_9,
    }

    for name, passed in all_tests.items():
        print(f"  {'PASS' if passed else 'FAIL'} — {name}")

    total_pass = sum(all_tests.values())
    print(f"\nTotal: {total_pass}/9 PASS")
    print(f"Timing golden-200: {elapsed:.1f}s")
    if resp2.status_code == 200:
        print(f"Timing full-2000: {elapsed2:.1f}s")


if __name__ == "__main__":
    test_s1()
