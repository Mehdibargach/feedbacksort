# BUILD Gameplan

> Template from The Builder PM Method — BUILD phase (start)

---

**Project Name:** FeedbackSort
**Date:** 2026-03-06
**Cycle Appetite:** 1 semaine
**MVP Features (from 1-Pager):**
1. CSV upload + auto-detection colonne texte
2. Classification 3 dimensions (sentiment, categorie, priorite)
3. Traitement par batch (20 avis par appel, concurrence)
4. Dashboard de synthese (distributions, top problemes)
5. Dataset de demo (2000 avis synthetiques avec ground truth)

**Riskiest Assumption (from 1-Pager):**
"Un LLM peut classifier des avis clients en sentiment, categorie et priorite avec plus de 85% de precision sur les 3 dimensions, sans donnees d'entrainement, simplement avec un prompt bien construit."

---

## Context Setup

**CLAUDE.md** du projet configure avec : Problem, Solution, Architecture Decisions du 1-Pager. Done.

---

## Walking Skeleton — "Le LLM classifie 10 avis"

> Le chemin le plus fin possible de bout en bout. On donne un CSV de 10 avis, le LLM classifie chacun en sentiment + categorie + priorite, et on mesure la precision.

**What it does :** On fournit un petit CSV d'avis clients (10 lignes). Le systeme detecte la colonne texte, envoie les avis au LLM avec un prompt de classification, et recoit pour chaque avis un triplet (sentiment, categorie, priorite) en JSON structure.

**End-to-end path :** CSV file → detection colonne texte → prompt classification → LLM (GPT-4o-mini) → JSON structure → resultats compares au ground truth

**Done when :** On peut classifier 10 avis avec au moins 80% de precision sur le sentiment, et le format de sortie est valide pour les 10 avis.

**Donnees de test :** 10 avis ecrits a la main avec ground truth connu (mix de sentiments, categories, et cas adversariaux).

**Micro-tests :**

| # | Test | Pass Criteria |
|---|------|---------------|
| WS-1 | CSV parsing + auto-detection | La colonne texte est identifiee automatiquement (pas de config manuelle). Fonctionne sur un CSV avec 3+ colonnes. |
| WS-2 | Format output valide | Les 10 avis retournent un JSON avec 3 champs : sentiment (Positive/Negative/Neutral), category (1 parmi les 7 definies), priority (Critical/High/Medium/Low). Zero valeur hors-liste. |
| WS-3 | Precision sentiment | >= 9/10 avis classifies correctement en sentiment (ground truth) |
| WS-4 | Precision categorie | >= 8/10 avis classifies correctement en categorie |
| WS-5 | Precision priorite | >= 7/10 avis classifies correctement en priorite |
| WS-6 | Adversarial : sarcasme | "Great, another crash. Love it." → Negative (pas Positive) |
| WS-7 | Adversarial : ambigu | "It's OK I guess" → Neutral (pas Positive) |

→ **RITUAL: Skeleton Check** — GPT-4o-mini classifie-t-il des avis avec une precision suffisante pour continuer ?
- Si NON → Tester GPT-4o. Si toujours NON → Pivot ou kill.
- Si OUI → Scope 1.

---

## Scope 1 — "Le pipeline complet"

**What it adds :** Dataset demo 2000 avis, traitement batch concurrent, dashboard de synthese, API endpoint. C'est le passage de "ca marche sur 10 avis" a "ca marche sur 2000 avis en 30 secondes avec un dashboard utile."

**Done when :** On peut envoyer un CSV de 2000 avis via l'API, recevoir la classification complete + un dashboard de synthese (distributions, top problemes), le tout en moins de 60 secondes pour moins de $0.10.

**Micro-tests :**

| # | Test | Pass Criteria |
|---|------|---------------|
| S1-1 | Dataset demo cree | 2000 avis synthetiques avec ground truth (sentiment, categorie, priorite). Distribution realiste : ~40% negatif, ~35% positif, ~25% neutre. Les 7 categories representees. |
| S1-2 | Batch processing | Les 2000 avis sont envoyes par paquets de 20 au LLM. Chaque batch retourne un JSON valide pour les 20 avis. |
| S1-3 | Traitement concurrent | 10 appels LLM en parallele. Le traitement complet des 2000 avis prend < 60 secondes. |
| S1-4 | Dashboard : distributions | 3 distributions calculees correctement : sentiment (% par label), categorie (% par label), priorite (% par label). Coherent avec le ground truth (ecart < 5%). |
| S1-5 | Dashboard : top 5 problemes | Les 5 combinaisons (categorie + priorite) les plus frequentes identifiees, avec nombre d'occurrences. |
| S1-6 | Dashboard : metriques resume | Nombre total d'avis, % negatifs, categorie #1, priorite moyenne. |
| S1-7 | API endpoint | POST /classify accepte un CSV (file upload) ou un nom de dataset demo. Retourne JSON : classifications + dashboard. |
| S1-8 | Precision golden dataset | Sur 200 avis avec ground truth : sentiment >= 90%, categorie >= 85%, priorite >= 80%. |
| S1-9 | Cout | Le traitement de 2000 avis coute < $0.10 (verifier usage OpenAI). |

---

## Scope 2 — "Le produit fini"

**What it adds :** Frontend Lovable (upload, dashboard visuel avec charts, dataset demo), deploy Render. Demo-ready.

**Done when :** Un visiteur peut aller sur l'URL, dropper un CSV ou choisir le dataset demo, et voir un dashboard complet : charts de distribution, top problemes, metriques.

**Micro-tests :**

| # | Test | Pass Criteria |
|---|------|---------------|
| S2-1 | Upload CSV | Drag & drop → le fichier est envoye au backend, la classification demarre, un loader s'affiche |
| S2-2 | Dataset demo | Bouton "Try with demo data" → classification + dashboard affiche en < 60s |
| S2-3 | Dashboard visuel | 3 charts : (1) distribution sentiment (pie/donut), (2) distribution categorie (bar horizontal), (3) distribution priorite (bar). Lisibles et propres. |
| S2-4 | Top problemes | Liste des 5 problemes principaux avec badge categorie + badge priorite + nombre d'avis |
| S2-5 | Mobile responsive | Dashboard lisible sur 375px width. Charts empiles verticalement. |
| S2-6 | Deploy Render | Backend live sur URL publique, frontend connecte, demo fonctionnelle |

---

## Exit Criteria (BUILD → EVALUATE)

- [ ] Les 5 features MVP fonctionnelles de bout en bout
- [ ] Riskiest Assumption testee (Skeleton Check passe)
- [ ] Open Questions du 1-Pager resolues ou converties en ADR
- [ ] Build Log a jour
- [ ] Pret pour evaluation formelle contre les Success Metrics
