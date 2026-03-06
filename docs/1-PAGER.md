# Builder PM 1-Pager

> Template from The Builder PM Method — FRAME phase

---

**Project Name:** FeedbackSort
**One-liner:** Drop 2000 avis clients, recois en 30 secondes un dashboard qui te dit exactement ou ca fait mal et quoi fixer en premier.
**Date:** 2026-03-06
**Builder PM Method Phase:** Classification / Prediction — side project #4/5 dans le portfolio Builder PM.

---

## Problem

1. **Lire 2000 avis a la main = 3 jours.** Un PM recoit du feedback de partout — App Store, Trustpilot, NPS, tickets support. Pour comprendre ce que disent les clients, il faut tout lire. Personne ne le fait. Le feedback finit dans un dossier "a traiter" et n'en sort jamais.

2. **Excel ne comprend pas le texte.** Tu peux trier un CSV par date ou par note. Mais "This app crashes every morning" et "Love the design but too expensive" — Excel ne sait pas que l'un parle d'un bug et l'autre du pricing. Le contenu textuel est invisible pour les outils classiques.

3. **Tout semble urgent.** Sans tri automatique, tout est un mur de texte. Le PM ne sait pas si le probleme numero un c'est les crashs (critique) ou les couleurs du bouton (cosmetique). Il traite ce qu'il voit en premier, pas ce qui compte le plus.

4. **Les patterns sont invisibles a l'oeil nu.** Sur 2000 avis, tu ne verras pas que "les plaintes pricing ont triple ce mois" ou que "80% des avis negatifs viennent d'un seul segment." Il faut un outil qui voit ce que l'humain rate.

### Comment le marche resout ca aujourd'hui

| Outil | Approche | Limite |
|-------|----------|--------|
| Lecture manuelle | Un PM lit chaque avis un par un | 3+ jours, pas scalable, biais de selection |
| Excel + filtres | Tri par note, mots-cles manuels | Ne comprend pas le contenu du texte |
| MonkeyLearn / Qualtrics XM ($300-1500/mo) | Classification ML parametrable | Cher, config complexe, fait pour les grosses equipes |
| ChatGPT (copier-coller) | Coller 50 avis dans le chat | Limite de contexte, pas de vue d'ensemble, pas reproductible |

**Le trou :** Aucun outil ne permet de dropper un CSV d'avis et d'obtenir en 30 secondes une vue claire : quels types de problemes, a quelle frequence, avec quelle gravite.

---

## User

- **Primary :** PM ou Head of Product qui recoit du feedback clients (App Store, NPS, Trustpilot, support) et doit prioriser les problemes.
- **Secondary :** Founder, Customer Success Manager, Growth Manager qui veut comprendre le sentiment client sans passer par l'equipe data.
- **Context :** Lundi matin (revue hebdo), fin de sprint (priorisation backlog), post-launch (monitoring sentiment), review trimestrielle (tendances).

---

## Solution

| Pain | Feature |
|------|---------|
| Lire 2000 avis a la main = 3 jours | Upload CSV → classification automatique de chaque avis en 30s |
| Excel ne comprend pas le texte | Le LLM (modele de langage) lit et comprend le contenu de chaque avis |
| Tout semble urgent | Tri par priorite (Critique / Haute / Moyenne / Basse) |
| Les patterns sont invisibles | Dashboard de synthese : distributions, top problemes, metriques |

---

## Riskiest Assumption

**"Un LLM peut classifier des avis clients en sentiment, categorie et priorite avec plus de 85% de precision sur les 3 dimensions, sans donnees d'entrainement, simplement avec un prompt bien construit."**

C'est le pari central : la classification "zero-shot" (= sans entrainement, le modele comprend la tache a partir d'instructions seules) peut-elle rivaliser avec un humain qui lirait chaque avis ?

Les 3 contraintes critiques :
- **Precision :** >= 85% sur chaque dimension (sentiment, categorie, priorite)
- **Coherence :** Un avis "App crashes every time" doit TOUJOURS etre classe Negatif + Bug + Critique, pas parfois Bug parfois Performance
- **Cout :** Classification de 2000 avis pour < $0.10 (batch via GPT-4o-mini)

---

## Classification — Les 3 dimensions

### Sentiment (3 valeurs)

| Label | Definition | Exemple |
|-------|-----------|---------|
| Positive | Le client est satisfait | "Best app I've used in years" |
| Negative | Le client est mecontent | "Terrible experience, deleted immediately" |
| Neutral | Pas de sentiment fort, constat factuel | "The app has a dark mode option" |

### Categorie (7 valeurs)

| Label | Definition | Exemple |
|-------|-----------|---------|
| Bug / Crash | L'app plante, freeze, ou a un bug technique | "App freezes when I open settings" |
| UX / Design | Navigation confuse, UI moche, ergonomie | "The navigation is confusing" |
| Performance | Lenteur, temps de chargement | "Takes 30 seconds to load" |
| Feature Request | L'utilisateur veut une fonctionnalite qui n'existe pas | "Wish I could export to PDF" |
| Pricing / Billing | Trop cher, facturation, abonnement | "Too expensive for what it offers" |
| Onboarding | Premiere utilisation difficile | "Took me 20 min to figure out how to start" |
| Praise | Compliment general, sans probleme specifique | "Absolutely love this app, 5 stars!" |

### Priorite (4 valeurs)

| Label | Definition | Critere de decision |
|-------|-----------|-------------------|
| Critical | L'app est inutilisable | Bug bloquant, perte de donnees, securite |
| High | Gros irritant, impacte l'experience | Bug frequent, fonctionnalite manquante critique |
| Medium | Irritant modere | Amelioration souhaitee, friction non bloquante |
| Low | Nice-to-have, cosmetique | Suggestion, preference personnelle |

---

## Scope Scoring

| Feature | Pain | Risk | Effort | Score | In/Out |
|---------|------|------|--------|-------|--------|
| CSV upload + auto-detection colonne texte | 3 | 1 | 1 | **3** | **IN** |
| Classification 3 dimensions (sentiment, categorie, priorite) | 3 | 3 | 2 | **4** | **IN** |
| Traitement par batch (20 avis par appel LLM) | 2 | 2 | 1 | **3** | **IN** |
| Dashboard de synthese (distributions, top problemes) | 3 | 2 | 2 | **3** | **IN** |
| Dataset de demo pre-charge (2000 avis synthetiques) | 2 | 3 | 1 | **4** | **IN** |
| CSV enrichi telechargeable (avis + labels) | 2 | 1 | 1 | **2** | OUT |
| Tendances temporelles (evolution mois par mois) | 2 | 1 | 2 | **1** | OUT |
| Mode "ask a question" sur le feedback | 1 | 1 | 3 | **-1** | OUT |
| Multi-langue (detection + classification) | 1 | 2 | 2 | **1** | OUT |

### MVP (Score >= 3) — 5 features

1. **CSV upload + auto-detection** de la colonne texte (avis)
2. **Classification 3 dimensions** : sentiment, categorie, priorite pour chaque avis
3. **Traitement par batch** : 20 avis par appel au LLM, traitement concurrent (= plusieurs appels en parallele pour aller plus vite)
4. **Dashboard de synthese** : distributions par sentiment/categorie/priorite, top 5 problemes par volume
5. **Dataset de demo** : 2000 avis synthetiques avec ground truth (= les bonnes reponses connues d'avance pour tester la precision)

### Out of Scope

- **CSV enrichi telechargeable** — Nice-to-have, pas necessaire pour valider la classification
- **Tendances temporelles** — Necessite une colonne date, complexifie le scope
- **Mode Q&A** — C'est DataPilot. FeedbackSort = classification, pas Q&A.
- **Multi-langue** — EN uniquement pour le MVP

---

## Success Metrics

| Metric | Target | How to Test |
|--------|--------|-------------|
| Precision sentiment | >= 90% | 200 avis avec ground truth, comparer LLM vs verite |
| Precision categorie | >= 85% | Idem — 200 avis, 7 categories possibles |
| Precision priorite | >= 80% | Idem — la priorite est plus subjective, seuil adapte |
| Zero hallucination | 0 categorie inventee hors des 7 definies | Verifier que chaque output est dans la liste autorisee |
| Latence 2000 avis | < 60 secondes | Chronometre le traitement complet (batch concurrent) |
| Cout 2000 avis | < $0.10 | Verifier usage OpenAI apres un run complet |

> La precision est testee sur un sous-ensemble de 200 avis manuellement verifies (= le "golden dataset"). C'est la meme approche que DataPilot et WatchNext : on sait la bonne reponse a l'avance, on mesure combien le LLM en trouve.

---

## Key Architecture Decisions

| Decision | Choix | Rationale |
|----------|-------|-----------|
| LLM | GPT-4o-mini (OpenAI) | Classification = tache simple. GPT-4o-mini suffit (pas besoin de GPT-4o comme DataPilot). ~20x moins cher. Si l'eval dit NO-GO, on upgrade. |
| Structured output | JSON mode avec schema fixe | Chaque avis → `{"sentiment": "...", "category": "...", "priority": "..."}`. Pas de parsing regex, pas d'erreur de format. |
| Batching | 20 avis par appel, 10 appels concurrents | 2000 avis / 20 = 100 appels. 10 en parallele = ~10 rounds de ~2s = ~20s. Bon equilibre entre vitesse et fiabilite. |
| Backend | FastAPI (Python) | Meme stack que DocuQuery, WatchNext, DataPilot. Consistance. |
| Frontend | Lovable (React + Tailwind) | Meme stack que les 3 projets precedents. |
| Deploy | Render ($7/mo) | Meme stack. |
| Dataset demo | Synthetique, 2000 avis, ground truth inclus | Permet une eval precise. Pas de donnees reelles = pas de probleme de confidentialite. |

---

## Adversarial Test Cases

> Le Walking Skeleton DOIT inclure au moins 1 cas difficile.

| Cas | Pourquoi c'est dur | Attendu |
|-----|-------------------|---------|
| Avis ambigu : "It's OK I guess" | Ni positif ni negatif. Le LLM doit resister a la tentation de choisir Positive. | Neutral + Low priority |
| Avis sarcastique : "Great, another crash. Love it." | Le sentiment litteral est positif, le vrai sentiment est negatif. | Negative + Bug + Critical |
| Avis multi-topic : "Love the design but way too expensive" | 2 sentiments opposes, 2 categories. Le LLM doit choisir le dominant. | Negative + Pricing + Medium (ou UX + Medium) |
| Avis tres court : "Broken" | Peu de contexte. Le LLM doit quand meme classifier. | Negative + Bug + High |
| Avis hors-sujet : "First review ever on the App Store lol" | Aucun feedback reel. | Neutral + Praise + Low |

---

## Open Questions

1. **Batch size optimal :** 20 avis par appel est une hypothese. Si le LLM perd en precision avec trop d'avis par batch, on reduit. A tester au Walking Skeleton.

2. **Subjectivite de la priorite :** Deux humains ne seraient pas d'accord sur "High vs Medium" pour beaucoup d'avis. Le seuil de 80% tient compte de cette subjectivite — mais il faudra peut-etre simplifier a 3 niveaux (Critical / Medium / Low) si la precision est trop basse.
