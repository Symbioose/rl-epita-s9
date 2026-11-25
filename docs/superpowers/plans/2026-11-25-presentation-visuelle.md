# Refonte visuelle de la soutenance

Objectif : 10 slides pour 10–15 minutes, avec une démonstration compréhensible et des visuels utiles.
Direction : fond ivoire, titres bleu nuit, bleu pour le modèle et orange pour l'adaptation.
Les illustrations de scènes sont des schémas issus de traces, jamais des captures prétendues du jeu.

- [x] Recomposer le fil : question, partie réelle, pipeline, données, loss, LoRA, résultats, historique, échec, conclusion.
- [x] Générer les illustrations vectorielles et les graphiques depuis les mesures sauvegardées.
- [x] Ajouter des notes « montrer / dire / transition » et isoler paramètres, métriques complètes et références en annexe.
- [x] Exporter HTML et PDF, inspecter chaque page, vérifier les données et publier sur le dépôt existant.

Fichiers concernés : presentation/build.py, assets/, index.html, notes.md, presentation.pdf,
annexes.html/pdf et scripts/export_pdf.py. Aucune modification du modèle ou des résultats expérimentaux.
