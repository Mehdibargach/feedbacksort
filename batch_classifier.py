"""
FeedbackSort — Batch classifier with concurrent processing.
Classifies reviews in batches of 50, with 10 concurrent API calls.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from classifier import classify_reviews

# Dedicated thread pool for API calls
_executor = ThreadPoolExecutor(max_workers=40)


def chunk_reviews(reviews: list[dict], batch_size: int = 25) -> list[list[dict]]:
    """Split reviews into batches."""
    return [reviews[i:i + batch_size] for i in range(0, len(reviews), batch_size)]


async def classify_batch_async(batch: list[dict], model: str = "gpt-4o-mini") -> list[dict]:
    """Classify a single batch asynchronously (runs sync call in thread pool)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, classify_reviews, batch, model)


async def classify_all_async(
    reviews: list[dict],
    batch_size: int = 25,
    max_concurrent: int = 40,
    model: str = "gpt-4o-mini",
) -> list[dict]:
    """Classify all reviews with concurrent batch processing.

    Args:
        reviews: list of dicts with 'id' and 'text' keys
        batch_size: number of reviews per API call
        max_concurrent: max parallel API calls
        model: OpenAI model

    Returns:
        list of classification results
    """
    batches = chunk_reviews(reviews, batch_size)
    all_results = []
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(batch):
        async with semaphore:
            return await classify_batch_async(batch, model)

    tasks = [process_batch(batch) for batch in batches]
    batch_results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, results in enumerate(batch_results):
        if isinstance(results, Exception):
            raise RuntimeError(f"Batch {i + 1}/{len(batches)} failed: {results}") from results
        all_results.extend(results)

    return all_results


def classify_all(
    reviews: list[dict],
    batch_size: int = 25,
    max_concurrent: int = 40,
    model: str = "gpt-4o-mini",
) -> list[dict]:
    """Synchronous wrapper for classify_all_async."""
    return asyncio.run(classify_all_async(reviews, batch_size, max_concurrent, model))
