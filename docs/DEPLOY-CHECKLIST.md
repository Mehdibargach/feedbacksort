# Deploy Checklist

> Template from The Builder PM Method — SHIP phase

**Project Name:** FeedbackSort
**Deploy Date:** 2026-03-07

---

## Infrastructure

- [x] Application deployed (API endpoint: https://feedbacksortopenai-api-key.onrender.com)
- [x] Web interface deployed (URL: Lovable)
- [x] Environment variables set (OPENAI_API_KEY en production)
- [x] CORS configured (allow_origins=["*"])

## Pre-Deploy Gate

- [x] Eval Gate passed — CONDITIONAL GO (0 BLOCKING fail, priorite 75% QUALITY PASS)

## Quality

- [x] Basic error handling / edge cases covered (CSV vide, colonnes manquantes, dataset inconnu)
- [x] Tested on mobile (responsive 375px)
- [x] Tested on Chrome + Safari
- [x] No API keys or secrets exposed in client code

## Documentation

- [x] README/CLAUDE.md updated with current state
- [x] Build Log entry for all 3 scopes completed
- [x] 3 Build Walkthroughs (WS, S1, S2) completed
- [x] Eval Report completed
- [x] 1-Pager updated with Eval Gate levels

## Post-Deploy

- [x] Demo URL works end-to-end (upload CSV → classification → dashboard)
- [ ] Shared with 2-3 test users for feedback
- [x] Project Dossier created
