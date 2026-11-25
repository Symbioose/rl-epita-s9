## 1. Un petit modèle apprend à jouer

≈ 40–50 secondes. Présenter la question et le protocole. Les diapositives de résultats ne contiennent que les conditions terminées. Vérifier que les douze conditions sont présentes avant d'annoncer une comparaison complète.

## 2. Une partie textuelle

≈ 40–50 secondes. Cet exemple sert à expliquer le format, ce n'est pas une sortie du modèle. TextWorld produit observation, score cumulé et fin. Notre récompense de transition est la différence des scores. Le modèle ne voit que le texte public. Source : Côté et al., https://arxiv.org/abs/1806.11532

## 3. Une politique avec mémoire

≈ 40–50 secondes. Expliquer la partial observability. La description et l'inventaire sont fournis à chaque pas : c'est une aide déclarée du protocole. On retire d'abord les échanges les plus anciens si le contexte dépasse 1024 tokens.

## 4. L'expert construit les exemples

≈ 40–50 secondes. TextWorld calcule une politique gagnante à partir de l'état symbolique. On exécute cette politique et ne garde que les parties gagnées. Aucune démonstration test n'est produite. Le solveur fournit les étiquettes, il n'entre pas dans les prompts. Source : https://textworld.readthedocs.io/en/stable/textworld.html

## 5. Même l’expert peut échouer

Environ 40 secondes. Le solveur répète unlock Canadian locker with Canadian latchkey. Les deux noms se recouvrent et le parseur n’avance pas. Nous filtrons les démonstrations perdantes, avec rapport de rejet. Aucun jeu test n’est retiré. Ce cas motive un contrôle de qualité des données plutôt qu’une confiance aveugle dans le solveur.

## 6. L'apprentissage par imitation

≈ 40–50 secondes. Faire le lien avec le TP LunarLander : observation -> action d'un expert. Ici l'action est une séquence de tokens. Les labels −100 ignorent le prompt et le padding. C'est du behaviour cloning, pas une optimisation par PPO. Une baisse de loss ne prouve pas que le modèle gagne.

## 7. LoRA : une petite correction

≈ 40–50 secondes. Expliquer les dimensions de A et B à l'oral. Pour une matrice illustrative 1024×1024, rang 16, on apprend 32768 paramètres plutôt que 1048576. Dans notre Qwen : 1 081 344 paramètres entraînés, soit 0,2184 % du modèle adapté. LoRA économise surtout gradients et états optimiseur ; la base reste en mémoire. Source : Hu et al., https://arxiv.org/abs/2106.09685

## 8. Des jeux séparés avant la collecte

≈ 40–50 secondes. 360 jeux compilés au total. Une démonstration avancée train est rejetée pour ambiguïté du parseur : 239 jeux train acceptés, 40 validation, 1371 transitions au total. Toutes les transitions d'un jeu restent dans le même split. Les empreintes vérifient l'intégrité. Des graines différentes ne garantissent pas une structure sémantique totalement nouvelle. Le checkpoint est choisi par loss de validation.

## 9. Deux entraînements réels sur T4

Environ 40 secondes. Le mélange augmente les données et le nombre de mises à jour. Trois époques configurées, batch 2, accumulation 8, learning rate 2e-4. Les temps désignent le fine-tuning, hors génération de jeux et évaluations. Les deux losses ne sont pas directement comparables car les ensembles de validation diffèrent.

## 10. L'expérience principale

≈ 40–50 secondes. La motivation est d'isoler l'effet de l'adaptation du modèle à la commande textuelle. Génération greedy, pas de correction vers la liste d'actions valides. Ajouter oracle comme contrôle de gagnabilité et aléatoire admissible comme référence privilégiée. Ces deux baselines ne disposent pas des mêmes informations que le LLM.

## 11. Le transfert vers des quêtes longues

≈ 40–50 secondes. Largeur de quête 1 puis 2 pour introduire des sous-objectifs combinés. Mesurer LoRA easy sur les deux niveaux, puis comparer LoRA mixed sur avancé. Mixed est un nouvel adaptateur appris depuis la même base Qwen, avec 1179 exemples contre 355. Il reçoit davantage de données et de mises à jour : un gain ne prouve pas un effet de la seule diversité. Les longueurs annoncées sont des paramètres de génération à vérifier par les traces oracle.

## 12. L'ablation de la mémoire

≈ 40–50 secondes. Technique avancée retenue : comparaison de stratégies de prompt. Hypothèse : l'historique aide à garder une progression et évite certaines répétitions. Il peut aussi distraire ou augmenter le coût. Le modèle est entraîné avec historique 4 : historique 0 crée un décalage d'inférence. Comparer les taux effectivement affichés. C'est une ablation à l'inférence, pas un second entraînement sans historique.

## 13. L'évaluation fait jouer l'agent

≈ 40–50 secondes. IC de Wilson sur les jeux. Il ne couvre pas la variation entre réentraînements. Avec 40 jeux, une victoire vaut 2,5 points. Invalidité = absence dans les actions admissibles, avec exceptions look/inventory : des synonymes peuvent être mal comptés. Une revisite peut être utile, donc l'indicateur boucle demande une lecture humaine.

## 14. Réussite sur des jeux non vus

Résultats issus des rollouts complets. Aléatoire et oracle disposent d'informations privilégiées. Les nombres au-dessus des barres indiquent victoires / jeux. Tous les coups, non-admissibles et boucles sont dans le rapport. Une seule graine de fine-tuning : les IC reflètent la variation des jeux, pas celle des entraînements.

## 15. Une erreur, puis une boucle

Environ 50 secondes. Le modèle échoue à prendre l’objet puis continue les étapes de l’objectif malgré le feedback négatif. Il répète ensuite plusieurs commandes jusqu’à la limite de 30 coups : 29 sont non admissibles. L’insecte est mentionné dans l’objectif, donc ce n’est pas une preuve d’objet halluciné. La trace complète figure dans l’archive, results/ECHECS.md explique la sélection déterministe. C’est un exemple de récupération insuffisante après une erreur, cohérent avec la couverture limitée des états par behaviour cloning ; cette cause n’est pas démontrée par une seule trace.

## 16. L’adaptation aide, le transfert reste fragile

≈ 40–50 secondes. Le fine-tuning aide sur les jeux simples ; le transfert de l’adaptateur simple aux quêtes avancées reste faible. L’entraînement mixte apporte davantage de données et de mises à jour : ne pas attribuer son gain à la seule diversité. Supprimer l’historique crée aussi un décalage avec les prompts d’entraînement. Une seule graine, grammaire contrôlée et objectif public explicite : ces résultats ne prouvent pas une planification universelle. Prochaine étape justifiable : collecte DAgger sur train, non implémentée ici.

## 17. Références

Sources complètes dans docs/REFERENCES.md. https://arxiv.org/abs/1806.11532 ; https://arxiv.org/abs/2106.09685 ; https://arxiv.org/abs/1011.0686 ; https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct. Jericho et ALFWorld sont des extensions possibles non implémentées.