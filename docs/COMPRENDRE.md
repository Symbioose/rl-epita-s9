# Comprendre chaque étape

## 1. Le jeu textuel

Une observation décrit la pièce, l'inventaire et la réponse à la dernière commande.
Une action est une chaîne comme `open chest`. L'environnement exécute cette action
et renvoie une nouvelle observation, un score cumulé et une indication de fin.
Dans nos logs, la récompense de transition est `score_après - score_avant`.
L'objectif consiste à gagner, avec une limite de 30 commandes, y compris les commandes
invalides. Demander l'inventaire compte donc aussi comme une commande.

L'état réel contient aussi les positions d'objets invisibles. Le joueur ne reçoit
que le texte public : c'est un problème partiellement observable. L'historique peut
servir de mémoire. Notre observation fournit aussi la description actuelle et
l'inventaire à chaque pas, ce qui facilite le problème. Il faut déclarer cette aide.

## 2. Pourquoi un modèle génératif ?

Un décodeur prédit le token suivant, puis recommence pour former une commande.
Il peut produire `take brass key from box`, y compris avec des noms nouveaux.
BERT est un encodeur : le faire scorer parmi des commandes prédéfinies serait
possible, mais cela changerait la tâche. Ici le modèle génère librement, sans
projection vers une action valide et sans solveur de secours.

## 3. Collecter une démonstration

TextWorld possède un état symbolique et sait calculer une politique gagnante.
À chaque pas de collecte, nous demandons sa prochaine commande, enregistrons
l'observation publique, exécutons la commande et conservons uniquement une partie
gagnée. Une ligne JSONL représente un exemple supervisé.

Exemple ILLUSTRATIF, pas un résultat d'exécution :

```json
{"game_id":"illustration","step":0,"history":[],"observation":{"objective":"Take the key.","description":"A key lies on the floor.","inventory":"Empty.","feedback":"Welcome."},"action":"take key"}
```

L'expert voit davantage d'informations que le modèle. C'est acceptable pour les
étiquettes, mais son plan ne doit jamais apparaître comme entrée de l'agent.
Dans un jeu partiellement observable, deux états symboliques peuvent aussi donner
des observations identiques et exiger des actions différentes : l'imitation a
alors une limite informationnelle.

## 4. Behaviour cloning

On entraîne une politique πθ(a | historique, observation) à reproduire l'expert.
La loss est la moyenne de `−log πθ(token_cible | contexte et tokens précédents)`
sur les tokens de la commande, avec les tokens de fin de message.

Les tokens du prompt et le padding ont une étiquette `−100`, ignorée par la
cross-entropy PyTorch. Sans ce masque, on entraînerait surtout le modèle à recopier
les longues descriptions. L'entraînement utilise les tokens experts précédents
(teacher forcing) ; pendant une partie, le modèle doit vivre avec ses propres erreurs.

Il s'agit d'apprentissage supervisé par imitation dans un environnement RL.
Nous n'optimisons pas directement le retour par PPO ou Q-learning. La récompense
sert à l'évaluation et à vérifier les démonstrations gagnantes.

## 5. LoRA

Une couche linéaire possède une matrice de poids W. Au lieu de modifier W, LoRA
apprend une correction ΔW = (α/r)BA, de rang au plus r. W reste figée.
Pour W de forme d_sortie × d_entrée, B a la forme d_sortie × r et A la forme
r × d_entrée. Il faut r(d_entrée+d_sortie) paramètres au lieu de d_entrée×d_sortie.

Exemple numérique : matrice 1024×1024, rang 16. W contient 1 048 576 paramètres ;
A et B ensemble en contiennent 32 768. Cette illustration ne donne pas le nombre
total entraînable de Qwen : le code mesure 1 081 344 paramètres dans nos adaptateurs,
soit 0,2184 % des 495 114 112 paramètres du modèle adapté.

Nous adaptons `q_proj` et `v_proj`, rang 16, α=32, dropout 0,05. LoRA réduit surtout
les gradients et états d'optimiseur à stocker. Le modèle de base occupe encore de
la mémoire. QLoRA ajouterait la quantification des poids de base ; notre code
implémente LoRA en précision mixte CUDA, sans QLoRA.

## 6. Pourquoi séparer les jeux ?

Séparer des lignes d'une même partie permettrait de retrouver la même carte au
test. Nous séparons les jeux avant collecte : 120 train, 20 validation, 40 test par
niveau. Toutes les transitions d'un jeu restent dans son split. Les graines et
empreintes sont vérifiées. Cela ne garantit pas des structures totalement nouvelles :
TextWorld conserve une grammaire et des règles communes. Parler de généralisation
sur jeux générés distincts, pas de généralisation universelle à tous les jeux.

## 7. Pourquoi la loss ne suffit pas ?

Une petite erreur peut changer la pièce atteinte, puis toutes les observations
suivantes. Une bonne prédiction sur les états experts peut donc coexister avec un
faible taux de victoire. C'est le décalage de distribution, ou covariate shift.
L'évaluation doit faire jouer le modèle jusqu'à une fin ou à la limite des coups.

DAgger serait une extension : faire jouer l'agent sur les jeux train, demander
l'action de l'expert sur ses états visités, ajouter ces exemples, puis réentraîner.
Cette technique n'est pas implémentée ici. L'approfondissement retenu est la
comparaison de stratégies de prompt, avec et sans historique, sur les deux niveaux.

## Exemple réel vérifié pendant la préparation

Le jeu d'entraînement `easy-10000` a été compilé sur Linux, puis joué localement
avec l'expert. La séquence `go south`, `close safe`, `lock safe with keycard`
aboutit à `won=True`. La trace complète est dans
`results/exemple_expert_train_10000.jsonl`. **C'est l'expert, pas le SLM.**
L'objectif public de ce jeu décrit déjà ces trois étapes. C'est une limite à
prendre en compte avant de parler de « planification ». Le premier prompt encodé
avec le tokenizer Qwen réel compte 631 tokens, dont le prompt est masqué pour la loss.
Cette mesure concerne un seul exemple, pas la distribution complète des données.
