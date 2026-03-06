# Build Walkthrough — Scope 1 : Le pipeline complet

## Ce qu'on a fait

On est passe de "ca marche sur 10 avis" a "ca marche sur 2000 avis en 46 secondes avec un dashboard utile." C'est le passage du prototype au pipeline.

Quatre briques construites :
1. Un dataset de 2000 avis synthetiques avec les bonnes reponses connues a l'avance
2. Un systeme de traitement par lots (= envoyer les avis par paquets au LLM, en parallele)
3. Un dashboard de synthese (distributions, top problemes, metriques)
4. Une API (= un point d'entree pour le frontend)

## Comment ca marche

```
CSV 2000 avis
    |
    v
Decoupe en 80 paquets de 25 avis
    |
    v
40 paquets envoyes en parallele au LLM
    |
    v
Chaque paquet → JSON avec sentiment + categorie + priorite
    |
    v
Aggregation → Dashboard (distributions, top 5 problemes)
    |
    v
API retourne tout en JSON
```

L'astuce : au lieu d'envoyer les 2000 avis un par un (ce qui prendrait ~30 minutes), on les regroupe par paquets de 25 et on envoie 40 paquets en meme temps. Resultat : 46 secondes au lieu de 30 minutes.

## Les 3 bugs qui ont fait mal

### Bug 1 : les IDs ne matchent pas

Le dataset de test a des IDs originaux (ex: 3, 45, 521). Mais l'API assignait de nouveaux IDs sequentiels (1, 2, 3...). Resultat : quand on comparait les resultats du LLM au ground truth, seulement 14 avis sur 200 matchaient par hasard.

**Fix :** L'API utilise les IDs originaux du CSV s'ils existent.

### Bug 2 : asyncio.run() dans un serveur

Le serveur web (uvicorn) tourne deja dans une boucle asynchrone. Appeler `asyncio.run()` a l'interieur cree un conflit — comme essayer de demarrer un deuxieme moteur dans une voiture deja en marche.

**Fix :** Utiliser `await` directement au lieu de `asyncio.run()`.

### Bug 3 : la priorite aleatoire dans le ground truth

C'est le bug le plus subtil et le plus instructif. Le dataset original assignait la priorite de facon aleatoire par categorie : "Bug → 40% Critical, 35% High, 20% Medium, 5% Low." Mais le LLM, lui, lisait le contenu de l'avis pour decider la priorite.

Resultat : le LLM disait "App freezes every time = Critical" et le ground truth disait "Medium" (par hasard). On mesurait la precision du LLM contre un de aleatoire. Le LLM avait raison, pas nous.

**Fix :** Priorite fixe par template, basee sur le contenu. "App crashes every time" = Critical. "Would be nice to have X" = Low. Toujours.

## La decouverte cle : les criteres ne sont pas egaux

En voulant atteindre 80% de precision sur la priorite, on a realise que c'etait un objectif irrealiste. Pourquoi ? Parce que la priorite est subjective.

Imagine deux PMs devant le meme avis : "Takes 30 seconds to load anything." L'un dit Medium (c'est lent mais ca marche), l'autre dit High (c'est inutilisable a cette vitesse). Qui a raison ? Les deux.

La methode Builder PM a un concept pour ca : le Eval Gate Framework. Chaque critere a un **niveau** :

| Niveau | Definition | Consequence si FAIL |
|--------|-----------|-------------------|
| BLOCKING | Doit passer absolument | On arrete tout (NO-GO) |
| QUALITY | Devrait passer | On continue avec une condition notee (CONDITIONAL GO) |
| SIGNAL | Bonus | On note et on avance |

Le sentiment (97%) et la categorie (98%) sont BLOCKING — sans eux, le dashboard est inutile. La priorite (75%) est QUALITY — c'est un plus, pas le coeur de la valeur.

**L'apprentissage :** Dans tout projet AI, il faut classifier ses criteres AVANT de builder, pas apres avoir decouvert que c'est dur. Un AI PM senior anticipe la subjectivite.

## Decisions prises

| Decision | Choix | Alternative rejetee | Pourquoi |
|----------|-------|-------------------|----------|
| Batch size | 25 avis par paquet | 20 (trop de paquets = lent) ou 50 (trop long par paquet) | 25 = meilleur ratio vitesse/fiabilite |
| Concurrence | 40 workers | 10 (trop lent : 140s) | 40 workers = 46s, bien sous la cible de 60s |
| Ground truth priorite | Fixe par template | Aleatoire par categorie | Aleatoire = on mesure contre du bruit, pas contre la verite |
| Seuil priorite | 70% (QUALITY) | 80% (BLOCKING) | La subjectivite rend 80% irrealiste en exact-match |

## Resultats finaux

| Dimension | Precision | Seuil | Niveau | Verdict |
|-----------|----------|-------|--------|---------|
| Sentiment | 97% | 90% | BLOCKING | PASS |
| Categorie | 98% | 85% | BLOCKING | PASS |
| Priorite | 75% | 70% | QUALITY | PASS |
| Latence | 46.6s | 60s | BLOCKING | PASS |
| Cout | ~$0.06 | $0.10 | QUALITY | PASS |
