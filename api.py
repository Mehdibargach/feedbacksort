"""
FeedbackSort — FastAPI API.
POST /classify: upload a CSV or use a demo dataset, get classifications + dashboard.
"""

import io
import os
import time

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from classifier import detect_text_column
from batch_classifier import classify_all_async
from dashboard import compute_dashboard

load_dotenv()

app = FastAPI(title="FeedbackSort API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_DATASETS = {
    "demo": "data/demo-reviews.csv",
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify")
async def classify_endpoint(
    file: UploadFile | None = File(None),
    dataset: str | None = Form(None),
):
    """Classify customer reviews from a CSV file or demo dataset.

    Args:
        file: uploaded CSV file (optional)
        dataset: name of a demo dataset (optional, e.g. "demo")

    Returns:
        classifications: list of {review_id, sentiment, category, priority}
        dashboard: distributions, top_problems, summary
        timing: processing time in seconds
    """
    start = time.time()

    # Load data
    if file:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
    elif dataset:
        if dataset not in DEMO_DATASETS:
            raise HTTPException(400, f"Unknown dataset: {dataset}. Available: {list(DEMO_DATASETS.keys())}")
        df = pd.read_csv(DEMO_DATASETS[dataset])
    else:
        raise HTTPException(400, "Provide either a file upload or a dataset name")

    # Detect text column
    try:
        text_col = detect_text_column(df)
    except ValueError as e:
        raise HTTPException(400, str(e))

    # Prepare reviews for classification (use original ID if present)
    has_id = "id" in df.columns
    reviews = []
    for idx, row in df.iterrows():
        rid = int(row["id"]) if has_id else idx + 1
        reviews.append({"id": rid, "text": str(row[text_col])})

    # Classify (use async directly since we're already in an event loop)
    classifications = await classify_all_async(reviews)

    # Dashboard (pass reviews for verbatims)
    dash = compute_dashboard(classifications, reviews)

    elapsed = time.time() - start

    return {
        "success": True,
        "total_reviews": len(reviews),
        "classifications": classifications,
        "dashboard": dash,
        "timing": round(elapsed, 2),
    }
