# Build Walkthrough — Scope 2 : Le produit fini

## Ce qu'on a fait

On est passe de "un pipeline qui tourne en API" a "un produit que quelqu'un peut utiliser." C'est le passage du backend au frontend, du JSON brut au dashboard visuel.

Deux choses construites :
1. Un frontend Lovable (React + Tailwind) connecte au backend Render
2. Un dashboard actionnable avec des vrais verbatims clients

## Comment ca marche

```
Utilisateur arrive sur le site
    |
    v
Choix : "Try demo" ou Upload CSV
    |
    v
Backend classifie 2000 avis (46s)
    |
    v
Frontend affiche le dashboard :
  - 4 cartes overview (Total, Positif, Negatif, Critical)
  - 3 charts (sentiment donut, categorie bar, priorite bar)
  - Top 5 problemes avec verbatims clients
```

L'utilisateur voit en un coup d'oeil : 40% des avis sont negatifs, le probleme #1 c'est Pricing/Billing HIGH (7.8%) avec les citations exactes des clients — "$15/month for this? Are you kidding me?"

## Le bug qui a fait mal

### Bug : Dashboard pas actionnable

Le dashboard V1 montrait des chiffres abstraits : "Top Category: Praise", des charts avec des indices (0, 1, 2) au lieu de noms, et zero verbatim client.

Le PM a reagi : "Pricing/Billing HIGH — mais de QUOI exactement ? Qu'est-ce qu'ils disent ?" C'est le test ultime d'un dashboard : est-ce qu'un PM peut prendre une decision en le regardant ?

**V1 :** "40% negatif, top categorie Praise" → Et alors ?
**V2 :** "Pricing/Billing HIGH : 157 avis (7.8%) — '$15/month for this? Are you kidding me?'" → Action claire.

**Fix :**
1. `dashboard.py` enrichi avec verbatims (3 citations par probleme) et breakdown complet (positif/negatif/neutre avec counts et %)
2. `api.py` modifie pour passer les textes originaux au dashboard
3. Prompt Lovable reecrit : labels corrects, 4 cartes overview, verbatims sous chaque probleme

## La decouverte cle : un dashboard sans verbatims est un dashboard inutile

Les chiffres disent OU ca fait mal. Les verbatims disent QUOI exactement. Un PM qui voit "Bug/Crash Critical: 99 avis" ne sait pas quoi faire. Un PM qui voit "App crashes on startup since the last update. Can't even open it." sait exactement quoi escalader a l'equipe engineering.

C'est la difference entre un tableau de bord et un outil de decision.

## La tagline

Premier essai : "Drop your reviews. See what hurts." — Le PM a dit : "ca fait amateur."

La vraie question : c'est quoi la valeur ? Pas le mecanisme (drop, classify, sort). La valeur c'est : quelqu'un lit les 2000 avis pour toi et te dit exactement ou ca coince.

**Tagline finale : "AI that reads every review so you don't have to."**

## Decisions prises

| Decision | Choix | Alternative rejetee | Pourquoi |
|----------|-------|-------------------|----------|
| Tagline | "AI that reads every review so you don't have to" | "Drop your reviews. See what hurts." | Trop amateur, ne communique pas la valeur |
| Top categorie | Top PROBLEM category (negatifs only) | Top categorie overall | "Top: Praise" est inutile — le PM veut savoir ce qui va MAL |
| Verbatims | 3 citations par probleme | Zero citation (chiffres seulement) | Chiffres = ou, verbatims = quoi. Les deux sont necessaires. |
| Design | Dark monochrome, cartes overview + charts + top problems | Charts seulement | Les cartes donnent la vue d'ensemble en 2 secondes |

## Resultats finaux

| # | Test | Resultat |
|---|------|----------|
| S2-1 | Upload CSV | PASS — drag & drop, loader, classification |
| S2-2 | Dataset demo | PASS — 2000 avis, dashboard affiche |
| S2-3 | Dashboard visuel | PASS — donut sentiment, bar categorie, bar priorite, labels corrects |
| S2-4 | Top problemes | PASS — 5 problemes, badges, counts, verbatims |
| S2-5 | Mobile responsive | PASS — charts empiles, lisible sur 375px |
| S2-6 | Deploy Render | PASS — backend live, frontend connecte |

**6/6 PASS.**
