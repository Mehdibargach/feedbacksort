# BUILD LOG — FeedbackSort

## Walking Skeleton — 2026-03-06

**Objectif :** Verifier que GPT-4o-mini peut classifier 10 avis clients en sentiment + categorie + priorite avec une precision suffisante.

**Ce qui a ete construit :**
- `classifier.py` — Module de classification : detection auto de la colonne texte + appel LLM avec prompt structure + validation des labels
- `test_ws.py` — Script de test des 7 micro-tests
- `data/ws-test-reviews.csv` — 10 avis de test avec ground truth

**Resultats : 7/7 PASS**

| Test | Critere | Resultat |
|------|---------|----------|
| WS-1 | CSV parsing + auto-detection | `review_text` detecte, 7 colonnes |
| WS-2 | Format output valide | 10/10 JSON valides, 0 hors-liste |
| WS-3 | Sentiment >= 9/10 | 9/10 (90%) |
| WS-4 | Categorie >= 8/10 | 10/10 (100%) |
| WS-5 | Priorite >= 7/10 | 9/10 (90%) |
| WS-6 | Sarcasme detecte | "Great, another crash" → Negative ✓ |
| WS-7 | Ambigu detecte | "It's OK I guess" → Neutral ✓ |

**Latence :** 8.70s pour 10 avis (1 appel LLM)

**Skeleton Check : OUI** — GPT-4o-mini classifie correctement. On continue.

**Bug corrige :** Le LLM retourne `{"reviews": [...]}` et non `{"results": [...]}`. Le parsing initial echouait (0 resultats). Fix : accepter n'importe quelle cle wrapper (reviews, results, classifications, ou premier array trouve).

**Ecarts non-bloquants :**
- Review 7 (feature request) : sentiment Neutral au lieu de Positive — discutable
- Review 9 (onboarding) : priorite High au lieu de Medium — subjectif
