# Protocole fixé avant les résultats

Toutes les expériences ci-dessous sont **prévues et implémentées**, pas encore
exécutées. La disponibilité de scripts ne prouve pas une performance.

## Jeux

| Niveau | Pièces | Objets demandés | Longueur quête | Largeur | Train / validation / test |
|---|---:|---:|---:|---:|---|
| easy | 3 | 5 | 3 | 1 | 120 / 20 / 40 |
| advanced | 6 | 10 | 7 | 2 | 120 / 20 / 40 |

Le générateur peut créer davantage d'objets nécessaires à une quête que le nombre
demandé. La largeur 2 introduit des sous-quêtes et des dépendances combinées.
Ce sont des paramètres de génération, pas une preuve empirique de difficulté :
contrôler les traces oracle et la longueur effective une fois les jeux générés.
Les jeux sont compilés en `.ulx`, et non joués depuis le JSON symbolique.

## Expériences et motivation

| Comparaison | Question | Ce qu'on peut conclure |
|---|---|---|
| Oracle / aléatoire admissible | Les jeux sont-ils gagnables, et le hasard suffit-il ? | Contrôle de l'environnement et référence faible |
| Base / LoRA easy, test easy | L'imitation améliore-t-elle la politique ? | Effet de l'adaptation sur la distribution simple |
| LoRA easy, easy / advanced | L'agent transfère-t-il à des tâches longues ? | Écart de performance sous changement de difficulté |
| LoRA easy / LoRA mixed, advanced | Des démonstrations complexes aident-elles ? | Effet d'un entraînement avec données supplémentaires |
| LoRA easy historique 4 / 0 | La mémoire récente aide-t-elle pendant l'inférence ? | Ablation du prompt pour un même checkpoint |

Le modèle mixed apprend sur easy+advanced : cette comparaison confond difficulté,
quantité de données et nombre de mises à jour. Elle ne permet pas d'attribuer un
progrès à la seule diversité. Une expérience à nombre de tokens et pas d'optimisation
égaux serait une extension intéressante. L'ablation historique 0 utilise un modèle
entraîné avec historique 4 : c'est une ablation d'inférence, pas deux modèles
entraînés dans les mêmes conditions.

L'aléatoire reçoit les commandes admissibles, qui sont une aide privilégiée.
L'oracle reçoit une politique gagnante. Les LLM ne reçoivent ni l'un ni l'autre.
Ces baselines servent de repères, pas de comparaison à information strictement égale.

## Hyperparamètres

Qwen2.5-0.5B-Instruct, LoRA q/v, rang 16, α 32, dropout 0,05,
learning rate 2e−4, trois époques, batch 2 et accumulation 8, soit batch effectif 16
sur un seul GPU, contexte maximal 1024, génération greedy jusqu'à 32 tokens.
Une graine de fine-tuning : 42. Choix du checkpoint par loss de validation minimale.
Aucune optimisation d'hyperparamètres guidée par le test.

## Mesures

- Réussite : fraction de jeux pour lesquels TextWorld renvoie `won=True`.
- IC 95 % de Wilson : incertitude liée à l'échantillon de jeux, pas à la variance
  de réentraînement. Avec seulement 40 jeux, 1 victoire représente 2,5 points.
- Coups moyens sur tous les épisodes, et séparément sur les réussites.
  La moyenne sur les seules réussites est `null` si aucune réussite.
- Invalidité opérationnelle : commande générée absente des actions admissibles,
  sauf `look` et `inventory`. Ce n'est pas une mesure parfaite de la validité du
  parseur : des synonymes compris peuvent être comptés invalides. Aucune projection
  vers l'action admissible n'est appliquée.
- Boucle : répétition d'un même quadruplet description/inventaire/feedback/action
  durant une partie. C'est un indicateur de revisite, parfois légitime.
- Troncature : limite de 30 commandes atteinte sans fin naturelle.

## Analyse des échecs à partir des traces

Lire des échecs de chaque condition et de chaque niveau, sans choisir seulement
les cas spectaculaires. Pour chaque trace, noter l'objectif, la première erreur,
la réponse de l'environnement et une catégorie : syntaxe, objet inexistant,
précondition manquante, oubli d'un sous-objectif, boucle, limite de coups.
L'hallucination d'objet demande une lecture manuelle, elle n'est pas automatiquement
déduite de toute invalidité. Le dossier `traces/` permet de relire les observations.

## Validation scientifique

Avant training : oracle gagne les jeux, prompts sans fuite, splits distincts,
vérification manuelle des tokens masqués. Après training : consulter la loss de
validation, vérifier que les poids LoRA existent, puis faire les rollouts.
Conserver aussi les échecs, la configuration et les coûts. Si le protocole change
après consultation du test, annoncer que ce test a servi au développement et créer
un nouveau jeu de test pour une conclusion confirmatoire.
