# Notes de soutenance

10 slides, environ 12 minutes. Les durées proposées totalisent environ 12 min 15 s.
Les annexes servent aux questions.

## 1. APPRENDRE À JOUER PAR LE TEXTE

Durée : 45 secondes.
MONTRER : le coffre et les commandes à droite.
DIRE : notre joueur est un petit modèle génératif Qwen2.5-0.5B-Instruct. Il lit du texte et répond par une commande. La question est de savoir si l’imitation d’un solveur améliore ses parties sur de nouveaux jeux.
TRANSITION : voici d’abord une partie réelle, avant de parler de réseaux de neurones.

## 2. Une quête, trois commandes

Durée : 75 secondes.
MONTRER : le joueur dans Cubicle, le déplacement vers Kitchenette, puis le coffre.
DIRE : dans cette partie du test, LoRA simple va à l’est, ouvre le type B locker puis prend la fly larva. Les noms et les commandes viennent de la trace easy-30001. Ce dessin représente les deux pièces observées, sans prétendre montrer toute la carte. Le texte décrit d’abord un coffre fermé, puis son contenu après ouverture.
La récompense est la différence entre scores successifs : 0, 0, puis 1. La victoire est vraie après la troisième commande. L’état complet est caché ; l’objectif, la description et l’inventaire sont fournis.
TRANSITION : comment apprendre à choisir ces commandes ?

## 3. L’expert enseigne, puis le modèle joue seul

Durée : 75 secondes.
MONTRER : suivre le trajet du solveur aux exemples, puis à LoRA ; descendre ensuite à la ligne d’évaluation.
DIRE : le solveur a accès à l’état symbolique pour trouver une bonne action. On exécute ses commandes et on garde les parties gagnantes. Le modèle reçoit uniquement les observations publiques et l’historique. Le walkthrough ne figure pas dans ses entrées.
C’est du behaviour cloning, comme le TP LunarLander : apprendre observation vers action à partir d’un expert. Ici une action est une suite de tokens. Nous utilisons un environnement RL, mais pas une optimisation par PPO ou Q-learning.
TRANSITION : pour mesurer un apprentissage réel, les jeux du test doivent rester séparés.

## 4. Des jeux nouveaux pour juger le modèle

Durée : 70 secondes.
MONTRER : la bande bleue train, orange validation et verte test, puis les deux tailles d’environnement.
DIRE : les nombres de la bande additionnent les deux niveaux. Les graines et empreintes sont distinctes. Toutes les transitions d’un jeu restent dans le même split. La validation sert à choisir le checkpoint ; le test mesure les performances finales.
Au niveau avancé, la largeur de quête passe aussi de 1 à 2, avec des sous-objectifs combinés. Les longueurs 3 et 7 sont des paramètres cibles ; les solutions effectives peuvent être plus courtes.
Une démonstration train avancée est rejetée : ambiguïté entre Canadian locker et Canadian limited edition locker. Le rejet et sa trace sont archivés ; aucun jeu test n’est retiré. On obtient 355 exemples simples ou 1179 mixtes.
TRANSITION : sur ces exemples, quelle partie du texte doit-on apprendre à produire ?

## 5. Apprendre la commande, token par token

Durée : 75 secondes.
MONTRER : le contexte gris et la commande bleue. Pointer les deux traits en dessous.
DIRE : le modèle apprend à rendre probable la commande experte, token par token, avec les tokens de fin de message. On masque le prompt et le padding avec des labels −100 : leur texte ne contribue pas à la cross-entropy. Le contexte sert à conditionner la réponse, sans devenir la cible à recopier.
À l’entraînement, il voit les tokens experts précédents, c’est le teacher forcing. En partie, il reçoit ses propres actions précédentes et leurs conséquences. Une petite erreur peut l’amener dans un état rarement vu pendant l’apprentissage : la loss seule ne mesure donc pas la capacité à gagner.
TRANSITION : on peut adapter Qwen sans réentraîner tous ses poids.

## 6. LoRA apprend une petite correction

Durée : 80 secondes.
MONTRER : la grande matrice grise W, puis les deux matrices fines A et B.
DIRE : LoRA ajoute une correction de faible rang à des poids figés. Le dessin illustre le principe, pas les dimensions exactes de Qwen. Pour une matrice sortie × entrée, B est sortie × r et A est r × entrée. On apprend r(sortie+entrée) paramètres au lieu de sortie×entrée.
Ici 1 081 344 paramètres reçoivent les gradients, soit 0,2184 % du modèle adapté. Nous adaptons q_proj et v_proj avec r16, alpha32. La base reste en mémoire ; ce n’est pas de la QLoRA.
Les deux adaptateurs repartent du même Qwen initial. Le simple utilise 355 exemples, le mixte 1179. Le mixte a davantage de données et de mises à jour : le comparer ne permet pas d’isoler la seule diversité. Temps réels du fine-tuning, hors évaluations.
TRANSITION : est-ce que cette adaptation change les parties sur les jeux non vus ?

## 7. L’adaptation aide, le transfert reste difficile

Durée : 100 secondes.
MONTRER : commencer par les barres Initial et LoRA simple à gauche. Comparer ensuite LoRA simple et LoRA mixte à droite.
DIRE : motivation 1, le fine-tuning aide-t-il ? Le modèle initial gagne 0/40, le simple 33/40 sur les quêtes simples. Motivation 2, ce modèle transfère-t-il ? Sur avancé, il tombe à 4/40. Motivation 3, de nouvelles démonstrations complexes aident-elles ? Le mixte atteint 31/40 sur avancé et 39/40 sur simple.
Les traits donnent les IC de Wilson à 95 % sur les jeux. Ils ne mesurent pas la variabilité entre réentraînements : nous n’avons qu’une graine. Le hasard choisit parmi les commandes admissibles, l’oracle reçoit un plan ; ils ont des informations privilégiées. Le SLM génère librement, sans correction vers la liste valide.
Les nombres viennent des rollouts sauvegardés. Les coups, invalidité et revisites sont en annexe et dans le rapport.
TRANSITION : une dernière expérience retire uniquement l’historique au même adaptateur.

## 8. Retirer l’historique fait chuter la réussite

Durée : 70 secondes.
MONTRER : les deux barres 33/40 et 1/40.
DIRE : cette ablation compare deux stratégies de prompt, notre technique avancée. Le checkpoint, les jeux et le décodage restent les mêmes. On retire les échanges précédents, en gardant observation, objectif, description et inventaire actuels.
Motivation : tester l’utilité de la mémoire récente. L’écart est grand, mais le modèle a été entraîné avec historique : le retirer crée un décalage d’entrée. Cela prouve la sensibilité de cet adaptateur, pas l’utilité universelle de toute mémoire. Nous n’avons pas entraîné un second modèle sans historique.
Sur avancé, le même modèle passe de 4/40 à 0/40. Le tableau complet reste en annexe.
TRANSITION : regardons maintenant comment une erreur peut s’accumuler.

## 9. Une action ratée peut bloquer toute la quête

Durée : 80 secondes.
MONTRER : parcourir les trois événements de gauche à droite, puis pointer la réponse négative du jeu.
DIRE : la première commande ne prend pas l’insecte. Le modèle va pourtant au sud et essaie ensuite de déposer un objet qu’il n’a pas. Il enchaîne des répétitions jusqu’à 30 coups, dont 29 non admissibles.
C’est une trace complète réelle et le premier échec simple par identifiant, pas un exemple inventé. L’insecte figure dans l’objectif : on ne peut pas appeler cela un objet halluciné. L’échec illustre un défaut de récupération après erreur. La faible couverture des états hors trajectoires expertes est une cause plausible du BC, sans être démontrée par ce seul cas.
L’invalidité est un proxy : des synonymes compris par le parseur peuvent être comptés non admissibles. Le diagnostic de boucle ignore le compteur de tours du feedback et recherche une répétition description/inventaire/commande.
TRANSITION : que peut-on conclure sans dépasser ce que les expériences montrent ?

## 10. Un petit modèle apprend, avec des limites

Durée : 65 secondes.
MONTRER : les deux grands nombres, puis revenir aux limites écrites en bas.
DIRE : le résultat positif est un adaptateur capable de gagner sur de nouveaux jeux générés. Le résultat négatif est le faible transfert du modèle simple et sa dépendance au contexte. Le modèle mixte reçoit davantage de données et d’updates : ne pas attribuer le gain uniquement à la complexité des démonstrations.
L’objectif public de TextWorld décrit souvent les étapes. Cela mesure largement le suivi de consignes, sans prouver une planification générale. Une seule graine de fine-tuning et des structures communes limitent les conclusions.
DAgger serait une suite : interroger l’expert dans les états visités par l’agent sur train, puis ajouter ces corrections. Nous ne l’avons pas implémenté.
CONCLURE : code, données, adaptateurs et traces sont archivés ; 18 tests Linux passent. Les paramètres, références et métriques sont en annexe pour les questions.