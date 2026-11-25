# Projet exécuté et livré — 25 novembre 2026

- Deux adaptateurs LoRA Qwen2.5-0.5B-Instruct entraînés réellement sur T4.
- 360 jeux TextWorld compilés, splits par jeu et empreintes contrôlés.
- 279 démonstrations gagnantes acceptées, un rejet train avancé documenté.
- 1371 transitions expertes rejouées avec succès dans TextWorld.
- 1179 exemples train mixtes et 192 validation contrôlés par le tokenizer Qwen.
- Poids LoRA finis ; empreintes des données conformes aux métadonnées.
- 24 conditions d'évaluation complètes : 480 épisodes test et 240 validation.
- Diagnostic de revisite recalculé depuis les traces ; résultats principaux inchangés.
- 18 tests réussis sous Linux, sans test ignoré, dont compilation et partie experte.
- Modules `src/` et tests conformes aux empreintes de la vérification Linux.
- Présentation HTML et PDF 16:9, graphique des résultats et notes orales.

GitHub Actions ne peut pas démarrer ses jobs à cause d’une restriction du compte.
La preuve de tests exécutés est le journal Linux Modal ; aucun badge CI vert n'est
revendiqué. Le Dockerfile est fourni mais n’a pas été exécuté sur ce Mac.

Voir `tests-linux.txt`, `tests-verification.json`, `verification_modeles.json`,
`tokenisation.json`, `verification_metriques.json`, `mesures.json` et `BILAN.md`.
Le coût facturé du compte et le pic de mémoire GPU ne sont pas mesurés.
Les performances ne sont pas une garantie sur d’autres distributions ou entraînements.
