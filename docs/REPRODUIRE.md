# Reproduire et vérifier

## Relire les expériences sans payer de GPU

Depuis la racine du dépôt, sur Linux avec Python 3.11 :

```bash
(cd reproducibility && sha256sum -c experiences.tar.gz.sha256)
tar -xzf reproducibility/experiences.tar.gz
python scripts/recompute_metrics.py
python scripts/report.py
python scripts/analyze_failures.py
```

Le contrôle doit réussir. Les chemins du manifeste sont relatifs à la racine
du dépôt. L’archive comprend les 360 jeux compilés, données expertes, transitions,
deux adaptateurs, journaux et parties. Les poids publics Qwen sont téléchargés
séparément lors d’une nouvelle inférence. Les checkpoints d’optimiseur sont exclus.

`results/tests-verification.json` conserve les empreintes du code et des tests
exécutés sous Linux. `results/verification_metriques.json` prouve que la correction
du diagnostic de revisite ne modifie aucune victoire, commande ou durée de partie.
Les empreintes des données et de la révision Qwen sont dans chaque `training.json`.

## Refaire les calculs

Installer selon README.md, puis utiliser un dossier neuf pour ne pas confondre
une nouvelle expérience et les preuves conservées :

```bash
python scripts/finish_project.py --help
python scripts/run_experiments.py --phase prepare --root artifacts_nouveau
python scripts/run_experiments.py --phase train --root artifacts_nouveau
python scripts/run_experiments.py --phase validation --root artifacts_nouveau
python scripts/run_experiments.py --phase test --root artifacts_nouveau
python scripts/report.py --root artifacts_nouveau/eval/test --output results/nouvelle_experience.md
```

La compilation TextWorld est sensible au système. Les graines et versions fixées
améliorent la reproductibilité sans promettre une identité bit à bit entre GPU,
versions CUDA et paquets transitifs. Ne pas modifier les hyperparamètres à partir
du test réservé. Prévoir un nouveau split pour toute nouvelle sélection de modèle.
