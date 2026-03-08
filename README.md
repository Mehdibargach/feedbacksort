# FeedbackSort

**Sort 2000+ customer reviews automatically — sentiment, category, priority.**

Drop a CSV of customer feedback. Get every review classified in ~47 seconds with a dashboard showing where it hurts — top problems, verbatim quotes, and distribution charts.

---

## How it works

```
CSV (2000 reviews) → Auto-detect text column → Batch 25/batch, 40 concurrent
                                                        ↓
                                                GPT-4o-mini (JSON mode)
                                                        ↓
                                    Sentiment + Category + Priority per review
                                                        ↓
                                    Dashboard: distributions, top 5 problems, verbatims
```

1. Your CSV is uploaded and the text column is auto-detected (longest average string length)
2. Reviews are split into batches of 25, processed by 40 concurrent workers
3. GPT-4o-mini classifies each review on 3 dimensions: sentiment, category, priority
4. Results are validated against whitelists (no hallucinated labels)
5. A dashboard is computed: distributions, top 5 problems (negative reviews grouped by category + priority), 3 verbatim quotes per problem

### Classification schema

- **Sentiment:** Positive, Negative, Neutral
- **Category:** Bug/Crash, UX/Design, Performance, Feature Request, Pricing/Billing, Onboarding, Praise
- **Priority:** Critical, High, Medium, Low

## Evaluation results

| Criterion | Level | Threshold | Result |
|-----------|-------|-----------|--------|
| Sentiment accuracy | BLOCKING | >= 90% | **97%** |
| Category accuracy | BLOCKING | >= 85% | **98%** |
| Priority accuracy | QUALITY | >= 70% | **75%** |
| Hallucination (off-list labels) | BLOCKING | 0 | **0** |
| Latency (2000 reviews) | BLOCKING | < 60s | **46.6s** |
| Cost (2000 reviews) | QUALITY | < $0.10 | **~$0.06** |

Evaluated on 200 stratified golden reviews with content-based ground truth. 9/9 regression tests PASS, 5/5 adversarial cases PASS (sarcasm, ambiguity, multi-topic). Full eval: [`docs/EVAL-REPORT.md`](docs/EVAL-REPORT.md)

## Tech stack

| Component | Technology |
|-----------|-----------|
| LLM | GPT-4o-mini (OpenAI), JSON mode, temperature=0 |
| Concurrency | ThreadPoolExecutor + asyncio.Semaphore (40 workers) |
| Backend | FastAPI (Python) |
| Frontend | React + Tailwind (Lovable) |
| Hosting | Render ($7/mo) |

## Local setup

```bash
# Clone and setup
git clone https://github.com/Mehdibargach/feedbacksort.git
cd feedbacksort
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add API keys
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run
uvicorn api:app --host 0.0.0.0 --port 8000
```

API endpoints:
- `GET /health` — health check
- `POST /classify` — classify a CSV of reviews (upload or demo dataset)

## Project structure

```
api.py                      ← FastAPI backend (2 endpoints)
classifier.py               ← LLM prompt, schema validation, text detection
batch_classifier.py         ← Concurrent batch processing (25/batch, 40 workers)
dashboard.py                ← Distributions, top 5 problems, verbatims
generate_demo_dataset.py    ← Synthetic dataset generator (2000 reviews)
data/
  demo_dataset.csv          ← 2000 synthetic reviews
  golden_dataset.csv        ← 200 stratified reviews for eval
docs/
  EVAL-REPORT.md            ← Full eval with failure analysis
  PROJECT-DOSSIER.md        ← Post-ship project dossier
```

## Built by

**Mehdi Bargach** — Builder PM · AI Products

[LinkedIn](https://www.linkedin.com/in/mehdi-bargach/)
