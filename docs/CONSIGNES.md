# Correspondance avec le sujet

| Attendu | Réalisation / preuve |
|---|---|
| TextWorld simple | 180 jeux easy, génération `games.py`, manifestes et binaires archivés |
| Trajectoires exploitables | Walkthrough exécuté ; données JSONL, masquage vérifié ; transitions RL exportées |
| SLM décodeur | Qwen2.5-0.5B-Instruct, génération libre de commandes |
| Fine-tuning | Deux adaptateurs LoRA réels ; poids, paramètres et versions archivés |
| Historique → prochaine commande | `common.py`, `tokenization.py`, `train.py` |
| Jeux non vus | Splits par jeu, graines et empreintes séparées ; 40 tests par niveau |
| Réussite, coups, invalidité | `evaluate.py`, tableau `results/rapport.md`, traces complètes |
| Niveau 2 | TextWorld avancé : 6 pièces, quête longueur 7, largeur 2 |
| Comparaison quantitative | Six agents sur les deux mêmes ensembles de test |
| Technique avancée | Ablation de stratégie de prompt : historique 4 contre 0 au même checkpoint |
| Analyse d'échecs | `results/ECHECS.md`, exemples commentés dans le bilan |
| Présentation claire | HTML et PDF, graphique, notes orales, notions expliquées |
| Expériences motivées | `EXPERIENCES.md`, hypothèse et limites de chaque comparaison |
| Code livré | Modules commentés, scripts, environnement, tests et archive de reproductibilité |

La taille de modèle n'est pas comparée ; ni PPO, ni DAgger, ni reward shaping ne
sont présentés comme implémentés. Le niveau 2 choisit TextWorld avancé et la
comparaison de prompts, parmi les options proposées dans le sujet. La sélection
du checkpoint utilise la validation ; aucun apprentissage n'utilise les jeux test.
