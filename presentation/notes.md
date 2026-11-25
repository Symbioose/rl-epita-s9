## 1. Un petit modèle apprend à jouer

0:00–0:40. Notre question est expérimentale : l'imitation de solutions expertes améliore-t-elle une politique sur des jeux nouveaux ? Annoncer d'emblée l'état réel : pipeline écrit, entraînement non exécuté dans la session de préparation. Ne pas annoncer de résultat sans logs.

## 2. Une partie textuelle

0:40–1:20. Cet exemple sert à expliquer le format, ce n'est pas une sortie du modèle. TextWorld produit observation, score cumulé et fin. Notre récompense de transition est la différence des scores. Le modèle ne voit que le texte public. Source : Côté et al., https://arxiv.org/abs/1806.11532

## 3. Une politique avec mémoire

1:20–2:00. Expliquer la partial observability. La description et l'inventaire sont fournis à chaque pas : c'est une aide déclarée du protocole. On retire d'abord les échanges les plus anciens si le contexte dépasse 1024 tokens.

## 4. L'expert construit les exemples

2:00–2:45. TextWorld calcule une politique gagnante à partir de l'état symbolique. On exécute cette politique et ne garde que les parties gagnées. Aucune démonstration test n'est produite. Le solveur fournit les étiquettes, il n'entre pas dans les prompts. Source : https://textworld.readthedocs.io/en/stable/textworld.html

## 5. L'apprentissage par imitation

2:45–3:35. Faire le lien avec le TP LunarLander : observation -> action d'un expert. Ici l'action est une séquence de tokens. Les labels −100 ignorent le prompt et le padding. C'est du behaviour cloning, pas une optimisation par PPO. Une baisse de loss ne prouve pas que le modèle gagne.

## 6. LoRA : une petite correction

3:35–4:25. Expliquer les dimensions de A et B à l'oral. Pour une matrice illustrative 1024×1024, rang 16, on apprend 32768 paramètres plutôt que 1048576. Ce n'est pas le total mesuré de Qwen. LoRA économise surtout gradients et états optimiseur ; la base reste en mémoire. Source : Hu et al., https://arxiv.org/abs/2106.09685

## 7. Des jeux séparés avant la collecte

4:25–5:05. Les nombres décrivent le protocole prévu. Toutes les transitions d'un jeu restent dans le même split. Les empreintes vérifient l'intégrité. Des graines différentes ne garantissent pas une structure sémantique totalement nouvelle. Le checkpoint est choisi par loss de validation.

## 8. L'expérience principale

5:05–5:50. La motivation est d'isoler l'effet de l'adaptation du modèle à la commande textuelle. Génération greedy, pas de correction vers la liste d'actions valides. Ajouter oracle comme contrôle de gagnabilité et aléatoire admissible comme référence privilégiée. Ces deux baselines ne disposent pas des mêmes informations que le LLM.

## 9. Le transfert vers des quêtes longues

5:50–6:40. Largeur de quête 1 puis 2 pour introduire des sous-objectifs combinés. Mesurer LoRA easy sur les deux niveaux, puis comparer LoRA mixed sur avancé. Mixed reçoit davantage de données et de mises à jour : un gain ne prouverait pas un effet de la seule complexité. Les longueurs annoncées sont des paramètres de génération à vérifier par les traces oracle.

## 10. L'ablation de la mémoire

6:40–7:20. Technique avancée retenue : comparaison de stratégies de prompt. Hypothèse : l'historique aide à garder une progression et évite certaines répétitions. Il peut aussi distraire ou augmenter le coût. Le modèle est entraîné avec historique 4 : historique 0 crée un décalage d'inférence. Aucun résultat de cette comparaison n'est encore disponible.

## 11. L'évaluation fait jouer l'agent

7:20–8:10. IC de Wilson sur les jeux. Il ne couvre pas la variation entre réentraînements. Avec 40 jeux, une victoire vaut 2,5 points. Invalidité = absence dans les actions admissibles, avec exceptions look/inventory : des synonymes peuvent être mal comptés. Une revisite peut être utile, donc l'indicateur boucle demande une lecture humaine.

## 12. Résultats : mesures non disponibles

8:10–9:00. Expliquer le blocage précis : résolution DNS de pypi.org refusée dans l'environnement local, dépendances absentes. Les tests unitaires valident les masques, les métriques et les protections de données ; ils ne remplacent pas un test du modèle. Le rapport sera calculé par scripts/report.py uniquement à partir des logs réels.

## 13. Comprendre un échec

9:00–9:45. Ce sont des catégories d'analyse prévues, pas des échecs déjà observés. Lire le premier écart et le feedback du jeu. Ne pas appeler toute action invalide hallucination : le modèle peut simplement utiliser un synonyme ou oublier une précondition. Le BC voit les états experts et peut manquer de couverture lorsqu'il s'égare.

## 14. Ce qu'il reste à mesurer

9:45–10:35. Modal T4, maximum 30 minutes par appel, aucun retry automatique, un seul conteneur. Ce n'est pas un plafond global de facturation. Vérifier les coûts après chaque phase et arrêter avant le budget utilisateur de 7 euros. Ne pas prétendre que le GPU a tourné. Source tarifaire : https://modal.com/pricing

## 15. Ce que l'expérience peut montrer

10:35–11:15. Ces phrases présentent les idées à tester, sans conclure à un gain non mesuré. Extension possible : DAgger pour collecter les actions expertes dans les états visités par l'agent sur train. Non implémenté. Source : Ross et al., https://arxiv.org/abs/1011.0686. Ouvrir les questions.

## 16. Références

Sources complètes dans docs/REFERENCES.md. https://arxiv.org/abs/1806.11532 ; https://arxiv.org/abs/2106.09685 ; https://arxiv.org/abs/1011.0686 ; https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct. Jericho et ALFWorld sont des extensions possibles non implémentées.