# TextGames Implementation Plan

**Goal:** construire un pipeline pédagogique reproductible de fine-tuning LoRA.
**Architecture:** modules Python séparés, backend TextWorld réel, JSONL auditable.
**Tech Stack:** Python 3.11, TextWorld, PyTorch, Transformers, PEFT, Modal.

## Étapes et vérification
- [ ] `src/textgame/games.py` : générer jeux avec graines distinctes par split et niveau.
  Vérifier le manifeste et les empreintes avec `python -m unittest discover -s tests`.
- [ ] `src/textgame/data.py` : collecter solutions gagnantes et bâtir prompts publics.
  Tester que les champs oracle ne passent jamais dans les observations.
- [ ] `src/textgame/train.py` : LoRA causal, loss sur action uniquement, padding masqué,
  checkpoint choisi par loss de validation et métadonnées d'entraînement.
- [ ] `src/textgame/evaluate.py` : rollouts complets, logs par transition, Wilson 95 %,
  moyenne des coups tous épisodes et épisodes réussis, diagnostic des boucles.
- [ ] `scripts/run_experiments.py` : exécuter les baselines et les ablations sur les
  mêmes jeux. Test final réservé après choix des hyperparamètres sur validation.
- [ ] `modal_app.py`, `Dockerfile`, `pyproject.toml` : environnement Linux reproductible,
  limites de temps GPU et récupération des artefacts sans secrets dans le dépôt.
- [ ] `docs/` et `presentation/` : guide étudiant, protocole, oral et état des résultats.
- [ ] Tests sans dépendances lourdes puis intégration TextWorld si installation possible.

## Contrainte découverte
Installation locale bloquée par la résolution DNS de pypi.org dans le bac à sable.
Le lancement GPU exige un accès réseau fonctionnel à Modal et Hugging Face.
