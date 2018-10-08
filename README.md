# Rapport TP substitution lexicale non supervisée
- TP1 pour le cours analyse sémantique
- DDL : 04/10
- Aude MARÊCHÉ, Chuyuan LI

## La tâche
Inspiré de la tâche [SemEval 2007 « Lexical substitution »](https://www.irit.fr/semdis2014/fr/task1.html), ce TP a pour objectif de trouver un substitut d'un mot cible dans une phrase qui n'altère pas le sens global de l'énoncé. Le résultat sera comparé avec les réponses fournies par les annotateurs avec le score OOT et BEST.


## La méthode

- FREDIST
    - FreDist fournit les 100 meilleurs substituts pour chaque mot sans prendre en compte le contexte (triés par ordre décroissant). Pour cette raison, on récupère directement les 10 premiers voisins des mots cibles en lisant le thésaurus, et on les stocke dans un dictionnaire.
    - ref : `class Fredist`


- FRWAC
    - lecture de thésaurus : lire le fichier et stocker le mot, sa catégorie, et les vecteurs à 700 dimensions dans un numpy array. (ref : `def read_frwak`)
    - génération de CBOW : pour chaque phrase on prend les mots pleins (catégories : a, v, adv, n) et on calcule la moyenne des vecteurs en fonction du choix des hyper-paramètres (full_window et cible) (ref : `def cbow`)
    - calcul de la similarité : pour calculer le cosinus entre le CBOW et les mots dans Frwac, on a d'abord normalisé tous les mots dans Frwac (ref `def normalise_frwac`), puis lancé le processus de chercher les 10 plus proches voisins (ref `def frwac_candidates_sub`).




## Résultats
| Thésaurus | Cible | Full-window | OOT | BEST | Fichier généré |
|:-------|:------:|:------:|:------:|:-------:|------:|
|FREDIST|comprise|non|0.23499|0.02012|fredist_subs.txt|
|FRWAC|comprise|non|0.01410|0.00072|frwac_subs_cible_no_full_window.txt|
|FRWAC|comprise|oui|0.00477|0.00051|frwac_subs_cible_full_window.txt|
|FRWAC|non_comprise|oui|0.00186|0|frwac_subs_no_cible_full_window.txt|

**Commentaires** : 

- On peut constater dans le tableau que le meilleur résultat est FREDIST, suivi par FRWAC cible comprise et sans contexte. Considérer les mots dans le contexte va effectivement faire baisser le score au lieu de l'améliorer. 
- La dernière combinaison donne le plus mauvais score. On remarque que dans ce cas les meilleurs substituts sont ceux qui sont plus proches des mots de la phrase et pas de la cible. Par exemple pour le mot **capacité** dans la phrase 35 : 

    - "Bon nombre d' entre eux , titulaires d' une <head>capacité</head> en angiologie , sont considérés par la Sécurité Sociale , comme des médecins généralistes à exercice particulier ( MEP ) au même titre que les homéopathes"

    - Les substituts proposés sont `homéopathe, homépathie, acupuncteur, allopathie, chiropracteur, acupuncture, ostéopathie, chiropractie, homeopathie, chiropraxie`.

    - Ces mots n'ont aucun rapport avec le mot cible *capacité* ; par contre ils sont proches de *homéopathe*, qui est dans la phrase.


## Questions et Réponses

(1) A priori à quoi sert d'inclure les mots du contexte ?

- Cela sert à prendre en compte les cas de polysémie. Par exemple le mot 'feux' dans les deux contextes suivants :  
    - *Le policier a été surpris par les feux nourris d'un groupuscule terroriste.*
    - Un substitut envisageable serait « tirs ».

- Par contre, dans la phrase :
    - *On y voit aussi comment sont organisés les pompiers forestiers, qui contrôlent les départs de feux de forêts.*
    - Le mot « incendies » serait plus adapté.
- Si on ne prend pas en compte les mots du contexte (et donc qu'on ne considère que le mot cible), on ne peut pas faire la différence entre ces deux cas.

(2) Est-ce qu'il peut être utile ou pas d'inclure pour le calcul du CBOW le vecteur du mot m ?

- Cela peut être utile, par exemple dans le cas ci-dessous :
    - *L'avion vole.* vs *L'oiseau vole.*
- Si on ne prend pas en compte les mots cibles *avion* et *oiseau*, les vecteurs moyennés pour ces deux phrases seront pareils ; et les mots substituts proposés seront identiques ; alors que les mots cibles se réfèrent à des entités différentes.


(3) Comment utiliser le score de similarité fourni dans FREDIST ?

- Comme mesure de confiance, c'est-à-dire avec un score plus élevé, on a plus de chance que ce soit un bon substitut.


(4) Commentaire pour la comparabilité

- Il y a 20 mots qui sont absents du thésaurus Fredist ; nous n'avons pas utilisé ceux de Frwac pour la substitution parce que nous considerons que cela permet pas de bien évaluer Fredist seul. Si le but était d'avoir une couverture maximale avec le meilleur score possible, il vaudrait mieux les utiliser.