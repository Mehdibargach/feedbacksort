# Build Walkthrough — Walking Skeleton

## Ce qu'on a fait

On a construit le coeur de FeedbackSort : un classifieur qui prend des avis clients et colle 3 etiquettes sur chacun — le sentiment (content, mecontent, neutre), la categorie (bug, UX, pricing...) et la priorite (critique, haute, moyenne, basse).

Imagine un douanier a l'aeroport. Chaque valise passe devant lui, il tamponne : "OK", "a fouiller", "urgent". Sauf qu'ici, les valises sont des avis clients, et le douanier c'est GPT-4o-mini (un modele de langage d'OpenAI, la version rapide et pas chere).

## Comment ca marche

```
CSV d'avis → Detection colonne texte → Prompt au LLM → JSON structure → Resultats
```

1. **Le CSV arrive** — n'importe quel fichier avec une colonne de texte
2. **On detecte automatiquement** quelle colonne contient les avis (la plus longue en moyenne)
3. **On envoie au LLM** avec un prompt precis : "classe chaque avis en sentiment/categorie/priorite, voici les labels autorises"
4. **Le LLM repond** en JSON structure — un triplet par avis
5. **On valide** que chaque label est dans la liste autorisee

## Ce qui a marche du premier coup

- **La detection de colonne** — l'heuristique "colonne texte la plus longue" fonctionne parfaitement
- **La precision** — 9/10 en sentiment, 10/10 en categorie, 9/10 en priorite. GPT-4o-mini est tres bon en classification.
- **Le sarcasme** — "Great, another crash. Love it." correctement identifie comme Negatif. Le LLM comprend l'ironie.
- **L'ambiguite** — "It's OK I guess" correctement identifie comme Neutre. Pas de biais vers Positif.

## Ce qui a merde

Le LLM retourne ses resultats dans un objet `{"reviews": [...]}`. Notre code cherchait `{"results": [...]}` ou `{"classifications": [...]}`. Resultat : 0 avis classifies au premier test.

**La lecon :** Quand tu demandes au LLM de repondre en JSON, il choisit le nom de la cle d'enveloppe. Il faut prevoir plusieurs noms possibles ou prendre le premier array trouve. C'est un pattern qu'on retrouve dans tous les projets — le LLM ne respecte pas toujours le format exact.

## Les 2 ecarts (discutables, pas faux)

| Avis | Attendu | Obtenu | Pourquoi c'est discutable |
|------|---------|--------|--------------------------|
| "Would be amazing if you could add PDF export" | Positive | Neutral | Une demande de feature n'est ni contente ni mecontente — les deux reponses se defendent |
| "Took me 20 min to create my first project" | Medium | High | C'est un vrai irritant. High n'est pas faux, c'est un desaccord d'interpretation |

## Decision cle

**GPT-4o-mini suffit pour la classification.** Pas besoin de GPT-4o (plus cher, plus lent). La classification est une tache simple pour un LLM — il ne genere pas de code, il ne raisonne pas en multi-etapes, il colle des etiquettes. C'est la difference fondamentale avec DataPilot (qui avait besoin de GPT-4o pour generer du code correct).

Si l'eval formelle dit NO-GO, on upgradera. Mais le signal du Skeleton est fort : 90%+ sur les 3 dimensions avec le modele le moins cher.
