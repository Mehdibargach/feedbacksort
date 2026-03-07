# FeedbackSort

## What this project is
AI-powered customer feedback classifier. Drop a CSV of reviews, get sentiment + category + priority for every review in 30 seconds, plus a dashboard showing exactly where it hurts.

## AI Typology
Classification / Prediction — side project #4/5 in the Builder PM portfolio.

## Architecture Decisions (from 1-Pager)
- **LLM**: GPT-4o-mini (OpenAI) — classification is a simple task, no need for GPT-4o
- **Structured output**: JSON mode with fixed schema per review
- **Batching**: 25 reviews per API call, 40 concurrent workers
- **Backend**: FastAPI (Python) — same stack as DocuQuery + WatchNext + DataPilot
- **Frontend**: Lovable (React + Tailwind) — same as previous projects
- **Deploy**: Render ($7/mo)
- **Dataset**: Synthetic 2000 reviews with ground truth labels

## Current Phase
BUILD DONE → EVALUATE next. WS (7/7), Scope 1 (8/9 CONDITIONAL GO), Scope 2 (6/6 PASS).

### Walking Skeleton — DONE (7/7 PASS)
- Classification 10 avis : sentiment 90%, categorie 100%, priorite 90%
- Sarcasme + ambiguite detectes correctement
- Latence : 8.70s pour 10 avis (1 appel LLM)
- Bug fixe : parsing JSON wrapper key (reviews vs results)

### Scope 1 — DONE (8/9 PASS — CONDITIONAL GO)
- Dataset demo 2000 avis synthetiques avec ground truth content-based
- Batch processing : 25 avis/batch, 40 concurrent workers
- Dashboard synthese : distributions + top 5 problemes + metriques
- API : POST /classify (file upload ou dataset demo)
- Precision : sentiment 97%, categorie 98%, priorite 75% (QUALITY, pas BLOCKING)
- Latence : 46.6s pour 2000 avis
- Cout : ~$0.06 pour 2000 avis
- Apprentissage : classifier les criteres (BLOCKING/QUALITY/SIGNAL) des le FRAME

### Scope 2 — DONE (6/6 PASS)
- Frontend Lovable : dark theme, 4 cartes overview, 3 charts, top 5 problemes avec verbatims
- Dashboard enrichi : verbatims (3 citations/probleme), breakdown complet, top PROBLEM category
- Deploy : backend Render + frontend Lovable connecte, demo fonctionnelle
- Mobile responsive : charts empiles, lisible 375px
- Apprentissage : un dashboard sans verbatims est un dashboard inutile

## Riskiest Assumption
"An LLM can classify customer reviews into sentiment, category, and priority with >85% accuracy across all 3 dimensions, without any training data, simply with a well-crafted prompt."

## Scope (5 IN, 4 OUT)
**IN:** CSV upload + auto-detect, Classification 3 dimensions, Batch processing, Dashboard synthesis, Demo dataset
**OUT:** CSV enrichi export, Tendances temporelles, Mode Q&A, Multi-langue

## Anti-patterns
- NEVER decompose into backend → frontend → integration
- Always vertical slices (Walking Skeleton → Scopes)

## Build Rules (applies to all projects)
1. Micro-test = gate, pas une etape. Code → Micro-test PASS → Doc → Commit.
2. Le gameplan fait autorite sur les donnees de test.
3. Checklist qualite walkthrough — audience non-technique.
4. Pas de mode batch.
5. Test first, code if needed.
6. UX dans les prompts — no jargon leaked to user.
7. PM Validation Gate — apres micro-tests PASS, AVANT commit : attendre GO explicite du PM.

## Build Checklist
See `/Users/mbargach/Claude Workspace/Projects/builder-pm/templates/build-checklist-claude.md`
