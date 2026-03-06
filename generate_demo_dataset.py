"""
Generate a synthetic demo dataset of 2000 customer reviews with ground truth labels.
Distribution: ~40% negative, ~35% positive, ~25% neutral.
All 7 categories represented. Mix of priorities.
Priority is FIXED per template (content-based, not random).
"""

import csv
import random

random.seed(42)

# Review templates: (template_text, priority)
# Priority is assigned based on the CONTENT of the template, not randomly.
TEMPLATES = {
    ("Negative", "Bug / Crash"): [
        ("App crashes every time I try to {action}. Completely unusable.", "Critical"),
        ("Keeps freezing when I {action}. Had to force quit {n} times today.", "High"),
        ("Lost all my {data} because the app crashed mid-{action}. Unacceptable.", "Critical"),
        ("Screen goes black whenever I {action}. Bug has been there for weeks.", "Critical"),
        ("App crashes on startup since the last update. Can't even open it.", "Critical"),
        ("The {feature} feature crashes immediately. Please fix this.", "High"),
        ("Constant crashes when using {feature}. Very frustrating.", "Critical"),
        ("App froze and I lost {n} minutes of work. Not cool.", "Critical"),
        ("Every time I try to {action}, the app just dies. So annoying.", "Critical"),
        ("Crash after crash after crash. When will you fix this?", "Critical"),
    ],
    ("Negative", "UX / Design"): [
        ("The navigation is so confusing. I can never find {feature}.", "Medium"),
        ("Why did you move the {feature} button? It was fine before.", "Medium"),
        ("The new design is terrible. Everything looks the same.", "Medium"),
        ("Can't figure out how to {action}. The UI is not intuitive at all.", "High"),
        ("Too many taps to do a simple {action}. Needs to be simpler.", "Medium"),
        ("The fonts are way too small. Can barely read anything.", "High"),
        ("Colors are ugly and the layout makes no sense.", "Medium"),
        ("I keep accidentally tapping the wrong button because they're too close together.", "Medium"),
        ("The menu structure is a maze. Just let me {action} directly.", "Medium"),
        ("Dark mode is broken — some text is invisible on dark backgrounds.", "High"),
    ],
    ("Negative", "Performance"): [
        ("Takes {n} seconds to load anything. Way too slow.", "High"),
        ("The app is incredibly laggy since the last update.", "High"),
        ("Loading times are ridiculous. I don't have time for this.", "High"),
        ("Everything runs so slow. Even scrolling is choppy.", "High"),
        ("It takes forever to {action}. Other apps do this instantly.", "High"),
        ("The search takes {n} seconds to return results. Painfully slow.", "Medium"),
        ("App uses too much battery. Drains {n}% in an hour.", "Medium"),
        ("Memory usage is insane. My phone heats up every time I use this.", "High"),
        ("The app takes {n} seconds just to start up. Way too heavy.", "High"),
        ("Syncing is extremely slow. Takes {n} minutes for a simple update.", "Medium"),
    ],
    ("Negative", "Pricing / Billing"): [
        ("${price}/month for this? Are you kidding me?", "High"),
        ("Way overpriced compared to {competitor}. Not worth it.", "Medium"),
        ("I was charged twice this month. No response from support.", "High"),
        ("The free tier is useless. You basically force people to pay.", "Medium"),
        ("Price went up from ${price_low} to ${price_high} with no new features.", "High"),
        ("Hidden fees everywhere. This is not transparent pricing.", "High"),
        ("I cancelled but was still charged. Want my money back.", "High"),
        ("The premium features are not worth the ${price}/month price tag.", "High"),
        ("Too expensive for what it does. {competitor} does the same for free.", "Medium"),
        ("Automatic renewal without warning. Shady business practice.", "High"),
    ],
    ("Negative", "Onboarding"): [
        ("Took me {n} minutes just to figure out how to get started.", "Medium"),
        ("No tutorial, no guide, nothing. Just dropped into the app blind.", "Medium"),
        ("The setup process has way too many steps. Almost gave up.", "Medium"),
        ("I still don't understand what half the features do after a week.", "Medium"),
        ("The onboarding tutorial is useless. Doesn't explain anything.", "Medium"),
        ("Had to watch YouTube videos just to learn basic {action}.", "Medium"),
        ("Why is the sign-up process so complicated? Just let me use the app.", "Medium"),
        ("First-time experience is awful. No guidance whatsoever.", "Medium"),
        ("The welcome screen has too much text and no visuals. Overwhelming.", "Medium"),
        ("I've been using the app for {n} days and still feel lost.", "Medium"),
    ],
    ("Positive", "Praise"): [
        ("Best app I've used in years. Simple, fast, and reliable.", "Low"),
        ("Absolutely love this app! It does exactly what I need.", "Low"),
        ("Five stars! The team behind this app really cares.", "Low"),
        ("This app has changed how I {action}. Couldn't live without it.", "Low"),
        ("Clean, intuitive, and fast. Exactly what an app should be.", "Low"),
        ("I've tried {n} other apps and this is by far the best one.", "Low"),
        ("Recommended this to all my friends. Everyone loves it.", "Low"),
        ("The best ${price} I spend every month. Worth every penny.", "Low"),
        ("This app is a game changer. So much better than {competitor}.", "Low"),
        ("Outstanding quality. You can tell the developers care about their users.", "Low"),
        ("Super intuitive. Figured everything out in {n} minutes.", "Low"),
        ("Love the attention to detail in this app. Everything just works.", "Low"),
        ("This is what every app should aspire to be. Perfect.", "Low"),
        ("Amazing app! It makes {action} so much easier.", "Low"),
        ("Been using this for {n} months and it just keeps getting better.", "Low"),
    ],
    ("Positive", "Feature Request"): [
        ("Great app! Would be even better with {feature} support.", "Medium"),
        ("Love it, but please add {feature}. That would make it perfect.", "Medium"),
        ("Almost perfect. Just needs {feature} and it's a 5-star app.", "Medium"),
        ("The app is amazing. My only wish is {feature} integration.", "Low"),
        ("Would love to see {feature} in a future update. Otherwise fantastic.", "Low"),
        ("Solid app. The only thing missing is the ability to {action}.", "Medium"),
        ("Really enjoy using this. {feature} would be the cherry on top.", "Low"),
        ("Great work! Any plans to add {feature}? That would be awesome.", "Low"),
    ],
    ("Neutral", "Praise"): [
        ("It's OK I guess. Nothing special but it works.", "Low"),
        ("Decent app. Does what it says.", "Low"),
        ("Average app. Not bad, not great.", "Low"),
        ("It works. Not much else to say.", "Low"),
        ("Just downloaded it. Will update my review later.", "Low"),
        ("First review on the App Store. Seems fine so far.", "Low"),
        ("It's a {category} app. It does {category} things.", "Low"),
        ("Meh. It's fine for what it is.", "Low"),
        ("Standard {category} app. Nothing stands out.", "Low"),
        ("Works as advertised. No complaints, no excitement.", "Low"),
    ],
    ("Neutral", "Feature Request"): [
        ("Would be nice to have {feature}. Not a dealbreaker though.", "Low"),
        ("The app works but I wonder if {feature} is on the roadmap.", "Low"),
        ("It does the basics. {feature} would be a nice addition.", "Low"),
        ("Could you consider adding {feature}? Just a suggestion.", "Low"),
    ],
}

# Fill-in values
ACTIONS = ["save", "export", "upload", "edit", "delete", "search", "sync", "share", "login", "sign up", "open settings", "view history", "update profile", "check notifications"]
FEATURES = ["PDF export", "dark mode", "offline mode", "keyboard shortcuts", "widgets", "Apple Watch support", "custom themes", "cloud backup", "multi-account", "two-factor auth", "calendar integration", "collaboration", "voice input", "templates"]
DATA_ITEMS = ["data", "files", "notes", "projects", "documents", "photos", "settings", "bookmarks"]
COMPETITORS = ["the competition", "similar apps", "alternatives", "other tools", "competing products"]
CATEGORIES_GENERIC = ["productivity", "task management", "note-taking", "planning", "organization"]
NUMBERS = list(range(2, 60))
PRICES = [5, 8, 10, 12, 15, 20, 25, 30]
PRICES_LOW = [3, 5, 8, 10]
PRICES_HIGH = [12, 15, 20, 25, 30]

# Target distribution
SENTIMENT_CATEGORY_COUNTS = {
    ("Negative", "Bug / Crash"): 200,
    ("Negative", "UX / Design"): 160,
    ("Negative", "Performance"): 140,
    ("Negative", "Pricing / Billing"): 160,
    ("Negative", "Onboarding"): 140,
    ("Positive", "Praise"): 500,
    ("Positive", "Feature Request"): 200,
    ("Neutral", "Praise"): 350,
    ("Neutral", "Feature Request"): 150,
}


def fill_template(template):
    """Fill a template with random values."""
    result = template
    result = result.replace("{action}", random.choice(ACTIONS))
    result = result.replace("{feature}", random.choice(FEATURES))
    result = result.replace("{data}", random.choice(DATA_ITEMS))
    result = result.replace("{n}", str(random.choice(NUMBERS)))
    result = result.replace("{competitor}", random.choice(COMPETITORS))
    result = result.replace("{category}", random.choice(CATEGORIES_GENERIC))
    result = result.replace("{price}", str(random.choice(PRICES)))
    result = result.replace("{price_low}", str(random.choice(PRICES_LOW)))
    result = result.replace("{price_high}", str(random.choice(PRICES_HIGH)))
    return result


def generate_dataset():
    reviews = []
    review_id = 1

    for (sentiment, category), count in SENTIMENT_CATEGORY_COUNTS.items():
        templates = TEMPLATES[(sentiment, category)]
        for _ in range(count):
            template_text, priority = random.choice(templates)
            text = fill_template(template_text)

            # Generate a date in 2025-2026
            year = random.choice([2025, 2025, 2025, 2026])
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d}"

            # Rating correlated with sentiment
            if sentiment == "Negative":
                rating = random.choices([1, 2, 3], weights=[50, 35, 15], k=1)[0]
            elif sentiment == "Positive":
                rating = random.choices([3, 4, 5], weights=[10, 30, 60], k=1)[0]
            else:
                rating = random.choices([2, 3, 4], weights=[20, 60, 20], k=1)[0]

            reviews.append({
                "id": review_id,
                "review_text": text,
                "date": date,
                "rating": rating,
                "expected_sentiment": sentiment,
                "expected_category": category,
                "expected_priority": priority,
            })
            review_id += 1

    # Shuffle
    random.shuffle(reviews)

    # Re-assign sequential IDs after shuffle
    for i, r in enumerate(reviews):
        r["id"] = i + 1

    return reviews


def main():
    reviews = generate_dataset()

    # Write full dataset
    with open("data/demo-reviews.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "review_text", "date", "rating", "expected_sentiment", "expected_category", "expected_priority"])
        writer.writeheader()
        writer.writerows(reviews)

    # Write golden subset (stratified 10% of each category, min 10)
    golden = []
    by_cat = {}
    for r in reviews:
        key = (r["expected_sentiment"], r["expected_category"])
        by_cat.setdefault(key, []).append(r)

    for key, items in by_cat.items():
        n = max(10, int(len(items) / 10))
        golden.extend(random.sample(items, min(n, len(items))))

    golden.sort(key=lambda x: x["id"])
    print(f"Golden subset: {len(golden)} reviews")

    with open("data/golden-200.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "review_text", "date", "rating", "expected_sentiment", "expected_category", "expected_priority"])
        writer.writeheader()
        writer.writerows(golden)

    # Stats
    print(f"\nDataset generated: {len(reviews)} reviews")
    from collections import Counter

    print("\nSentiment:")
    for s, c in Counter(r["expected_sentiment"] for r in reviews).most_common():
        print(f"  {s}: {c} ({c/len(reviews)*100:.1f}%)")

    print("\nCategory:")
    for s, c in Counter(r["expected_category"] for r in reviews).most_common():
        print(f"  {s}: {c} ({c/len(reviews)*100:.1f}%)")

    print("\nPriority:")
    for s, c in Counter(r["expected_priority"] for r in reviews).most_common():
        print(f"  {s}: {c} ({c/len(reviews)*100:.1f}%)")


if __name__ == "__main__":
    main()
