# Macro Retro — FeedbackSort V1

> Template from The Builder PM Method — post-SHIP ritual
> Bridge between V(n) and V(n+1). If skipped, the macro-loop breaks.

**Project:** FeedbackSort
**Date:** 2026-03-07
**Version:** V1
**Eval Gate:** CONDITIONAL GO
**Build Duration:** ~1.5 jours

---

## 1. Harvest — What came out of the Eval Gate?

### Conditions (from CONDITIONAL GO)

| # | Condition | Level | Impact |
|---|-----------|-------|--------|
| C1 | Priorite 75% (seuil revise de 80% a 70%) | QUALITY | Faible — High ↔ Medium confusion, les deux sont defensibles. Les verbatims compensent. |
| C2 | Dataset synthetique uniquement (pas de vrais avis testes) | SIGNAL | Inconnu — la classification tient sur du texte controle, pas encore teste "wild." |

### Build Learnings (product-affecting)

1. **Classifier les criteres d'eval des le FRAME, pas pendant le BUILD.** On a decouvert que la priorite est subjective APRES avoir fixe un seuil de 80%. Un AI PM senior aurait anticipe : sentiment = objectif (BLOCKING), priorite = subjectif (QUALITY). Le Eval Gate Framework avec niveaux (BLOCKING/QUALITY/SIGNAL) devrait etre rempli dans le 1-Pager, pas en reaction a un echec.

2. **Le ground truth doit etre content-based, pas aleatoire.** Le dataset original assignait la priorite par tirage aleatoire pondere ("Bug → 40% Critical, 35% High..."). Le LLM classifiait par contenu — et avait raison. On mesurait la precision contre du bruit. Fix : priorite fixe par template. Lecon : un ground truth mal concu invalide toute l'evaluation.

3. **Un dashboard sans verbatims est un dashboard inutile.** Le PM a reagi a la V1 : "Pricing/Billing HIGH — mais de QUOI exactement ?" Les chiffres disent OU ca fait mal. Les verbatims disent QUOI. Sans les deux, pas de decision possible.

### User/PM Signals

- Le PM a rejete la tagline "Drop your reviews. See what hurts." — trop mecanisme, pas assez valeur. "AI that reads every review so you don't have to" = la valeur.
- Le PM a challenge "Top Category: Praise" — inutile. Remplace par "Top Problem Category" (negatifs seulement).
- Le PM a demande "qu'aurait fait un AI PM senior ?" sur la priorite — a mene au Eval Gate Framework avec niveaux de criteres. C'est devenu un element central de la methode.

---

## 2. Decision — STOP

**STOP** — Le produit est demo-ready. Les conditions sont mineures (priorite QUALITY atteint, dataset synthetique = limitation connue). Le ROI d'une V2 est faible compare au cout d'opportunite.

### Justification

| Critere | Analyse |
|---------|---------|
| Conditions bloquantes ? | Non — 0 BLOCKING fail. |
| Valeur supplementaire a debloquer ? | Faible — CSV export et filtres seraient des "nice to have", pas des game changers pour le portfolio. |
| Cout d'opportunite ? | Eleve — EvalKit (#5) est le dernier projet. Il couvre la typologie AI Evaluation, la plus differenciante pour le positionnement "Build, Evaluate & Ship." |
| Materiel livre suffisant ? | Oui — 3 walkthroughs, Eval Gate Framework avec niveaux, ground truth content-based, verbatims insight. |
| Objectif portfolio atteint ? | Oui — Classification/Prediction demontre. 4/5 typologies couvertes. |

### Comparaison avec les autres STOP

| Projet | Decision | Raison principale |
|--------|----------|-------------------|
| DocuQuery | STOP | RAG demontre, 0 users, 4 projets restants |
| DataPilot | STOP | 87.5% suffisant, conditions = tweaks, 2 projets restants |
| WatchNext V2 | STOP | Rendements decroissants, conditions SIGNAL |
| **FeedbackSort** | **STOP** | **Classification demontree, conditions mineures, 1 projet restant** |

Le pattern est clair : chaque projet STOP libere du temps pour le suivant. La valeur marginale d'une V2 est inferieure a la valeur d'un nouveau projet qui couvre une nouvelle typologie.

---

## 3. Bridge — N/A (STOP)

Pas de V2 prevue. Les recommendations V2 (CSV export, filtres, test vrais avis, simplifier priorite a 3 niveaux) sont documentees dans l'Eval Report pour reference.

---

## Completion Checklist

- [x] Eval Report reviewed
- [x] Decision documented with justification (STOP)
- [x] Bridge section: N/A (STOP)
- [x] Project Dossier updated
- [x] CLAUDE.md updated
- [x] MEMORY.md updated (FeedbackSort → SHIP)
- [x] GitHub pushed (`ad2f892`)
