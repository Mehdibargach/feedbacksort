# Project Dossier — FeedbackSort

> Template from The Builder PM Method — post-SHIP

---

**Project Name:** FeedbackSort
**One-liner:** AI that reads every review so you don't have to.
**Live URL:** Lovable frontend + https://feedbacksortopenai-api-key.onrender.com (API)
**GitHub:** https://github.com/Mehdibargach/feedbacksort
**Date Shipped:** 2026-03-07
**AI Typology:** Classification / Prediction (#4/5 Builder PM portfolio)

---

## 1-Pager Summary

**Problem:** Un PM recoit 2000 avis clients. Les lire a la main = 3 jours. Excel ne comprend pas le texte. Tout semble urgent. Les patterns sont invisibles.

**User:** PM ou Head of Product qui recoit du feedback (App Store, NPS, Trustpilot, support) et doit prioriser les problemes.

**Solution:** Drop un CSV de 2000 avis → classification automatique en sentiment (Positive/Negative/Neutral) + categorie (7 valeurs) + priorite (Critical/High/Medium/Low) → dashboard de synthese avec distributions, top 5 problemes, et verbatims clients.

---

## Architecture Diagram

```
CSV 2000 avis
    |
    v
FastAPI (api.py) — CSV parse + auto-detect colonne texte
    |
    v
Batch Classifier (batch_classifier.py) — 80 batches x 25 avis, 40 concurrent
    |
    v
GPT-4o-mini (OpenAI) — JSON mode, schema fixe par avis
    |
    v
Dashboard (dashboard.py) — distributions + top 5 + verbatims
    |
    v
Frontend Lovable (React + Tailwind) — dark theme, charts, cartes
```

**Stack:** FastAPI + GPT-4o-mini + Lovable + Render

---

## Key ADRs

| Decision | Choice | Why |
|----------|--------|-----|
| LLM | GPT-4o-mini (pas GPT-4o) | Classification = tache simple. 20x moins cher. 97% sentiment, 98% categorie. |
| Batch config | 25 avis/batch, 40 concurrent | Optimal apres tests : 46.6s (vs 140s avec 20/10). |
| Ground truth priorite | Fixe par template (content-based) | L'alternative (aleatoire par categorie) mesurait la precision contre du bruit. Le LLM avait raison, pas le ground truth. |
| Seuil priorite | 70% QUALITY (pas 80% BLOCKING) | La priorite est inherement subjective. 2 humains ne seraient pas d'accord sur ~25% des avis. Classifier les criteres (BLOCKING/QUALITY/SIGNAL) evite de bloquer sur une dimension non-bloquante. |

---

## Eval Results

| Metric | Target | Actual | Level | Verdict |
|--------|--------|--------|-------|---------|
| Sentiment | >= 90% | 97% | BLOCKING | PASS |
| Categorie | >= 85% | 98% | BLOCKING | PASS |
| Priorite | >= 70% | 75% | QUALITY | PASS |
| Hallucination | 0 | 0 | BLOCKING | PASS |
| Latence (2000) | < 60s | 46.6s | BLOCKING | PASS |
| Cout (2000) | < $0.10 | ~$0.06 | QUALITY | PASS |

**Decision : CONDITIONAL GO → SHIP**

---

## What I Learned

1. **Technical:** Le batch concurrent (ThreadPoolExecutor + asyncio Semaphore) est le pattern standard pour les appels LLM en volume. 40 workers = le sweet spot pour OpenAI avant throttling. asyncio.run() ne marche pas dans un serveur ASGI — il faut await directement.

2. **Product:** Un dashboard sans verbatims est un dashboard inutile. Les chiffres disent OU ca fait mal. Les verbatims disent QUOI exactement. "Pricing/Billing HIGH: 157 avis" ne fait rien bouger. "$15/month for this? Are you kidding me?" fait bouger.

3. **Process:** Classifier les criteres d'eval (BLOCKING/QUALITY/SIGNAL) des le FRAME, pas apres avoir decouvert que c'est dur en BUILD. La priorite est subjective — un AI PM senior l'anticipe. Un seuil unique pour toutes les dimensions masque la difference entre objectif (sentiment) et subjectif (priorite).

4. **Data:** Le ground truth doit etre content-based, pas aleatoire. Un ground truth aleatoire mesure la precision contre du bruit — le LLM peut avoir raison et quand meme "echouer."

---

## Content Extracted

- [x] Book chapter: Ch.4 (Classification typology) + Ch.6 (Eval Gate with BLOCKING/QUALITY/SIGNAL levels)
- [ ] LinkedIn post: "Un dashboard sans verbatims est un dashboard inutile" / "La priorite est subjective — et c'est OK"
- [ ] Newsletter: FeedbackSort build walkthrough (pipeline + eval)
- [x] STAR story: "Built an AI classifier that reads 2000 reviews in 46s with 97% accuracy — and learned that evaluating priority is harder than evaluating sentiment because subjectivity isn't a bug, it's a feature."
