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
Les jeux sont compilés en `.z8`, et non joués depuis le JSON symbolique.

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
- Invalidité opérationnelle : commande générée absente des actions admissibles
  après comparaison insensible à la casse,
  sauf `look` et `inventory`. Ce n'est pas une mesure parfaite de la validité du
  parseur : des synonymes compris peuvent être comptés invalides. Aucune projection
  vers l'action admissible n'est appliquée.
- Boucle : répétition d'un même triplet description/inventaire/commande
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

## Une aide publique à déclarer

Le texte d'objectif généré par TextWorld peut expliciter plusieurs étapes de la
quête. Notre agent a accès à cet objectif, comme tout joueur. Cela facilite la
suivie de consignes et ne démontre pas à lui seul une capacité à inventer un plan.
Le champ caché `policy_commands` reste réservé à l'expert. Une future ablation
pourrait remplacer l'objectif détaillé par une formulation courte, mais elle
changerait le benchmark et demanderait une nouvelle comparaison contrôlée.

## Coût de préparation et reprise

Les jeux sont compilés sur CPU dans deux processus séparés, avec des graines
explicites. L'ordre de fin des tâches ne change pas le manifeste final, trié par
graine. En cas d'arrêt, le programme réutilise les binaires valides dont l'UUID
TextWorld correspond aux paramètres demandés. Il vérifie le checksum Z-machine et
conserve les empreintes du binaire et du JSON. Cela ne modifie ni les splits ni les
quêtes et évite de recommencer la compilation pendant un appel GPU.

## Format de la sortie du SLM

La commande exécutée est la première ligne non formatée de la réponse : les
espaces de bord et les backticks sont retirés. Les métriques portent sur cette
commande effectivement envoyée au jeu. Aucune commande n'est remplacée par une
action de la liste admissible et aucun oracle ne corrige le modèle pendant ses parties.

## Filtrage de l'expert réellement nécessaire

Sur le jeu train `advanced-110084`, l'expert propose de déverrouiller `Canadian
locker`, mais le parseur demande de choisir entre cet objet et `Canadian limited
edition locker`. Le solveur répète la même commande sans avancer. Ce problème a
été reproduit et sa trace est conservée dans `results/diagnostic_oracle_110084.jsonl`.

La collecte conserve uniquement les épisodes experts gagnants. Chaque rejet est
listé dans `collection-report.json`, avec le jeu, le split et une trace complète.
Les effectifs **après filtrage** sont calculés dans `results/donnees.json`. Aucun
jeu du test n'est supprimé pour cette raison : la baseline oracle peut donc échouer
elle aussi. Ses résultats ne sont pas une garantie que tous les jeux sont faciles
ou sans ambiguïté. Les exceptions d'exécution continuent à interrompre le pipeline.

## Budget de contexte vérifié sur les données

L'audit initial a trouvé deux observations train avancées dépassant 1024 tokens
(`advanced-110005`, `advanced-110047`, au pas initial), à cause de la bannière ASCII
imprimée au reset. Le pipeline retire d'abord les tours d'historique anciens. Si
l'observation seule dépasse encore le budget, il retire uniquement la bannière
composée de caractères graphiques et l'objectif dupliqué dans le feedback.
L'objectif reste entièrement présent dans son propre champ, ainsi que la description
et l'inventaire. Un texte narratif ou un avertissement n'est jamais supprimé par
cette règle ; si le budget reste dépassé, une erreur explicite est levée.

Le même traitement existe à l'entraînement et en inférence. Après correction,
1179/1179 exemples train mixtes et 192/192 exemples validation sont encodables.
Les 355 exemples train simples et 60 exemples validation simples sont exactement
inchangés au niveau des tokens. Le premier checkpoint simple est donc conservé.
Les audits avant et après sont dans `results/tokenisation-initiale.json` et
`results/tokenisation.json`. Aucun résultat du test n'a servi à cette correction.

## Vérification de l'indicateur de revisite

Avant les évaluations, l'inspection des observations a montré que le feedback
contient un compteur de coups. L'inclure dans la signature aurait masqué des
allers-retours valides, car ce compteur change à chaque tour. La version 2 mesure
les répétitions de description, inventaire et commande (sans tenir compte de la
casse). Une revisite peut rester légitime : c'est un diagnostic, pas une preuve
qu'une partie est irrécupérable.

`scripts/recompute_metrics.py` recalcule ce diagnostic à partir des traces. Il
vérifie que les victoires, nombres de coups et commandes non admissibles restent
strictement inchangés. Les sorties du modèle ne sont pas rejouées ni sélectionnées.
