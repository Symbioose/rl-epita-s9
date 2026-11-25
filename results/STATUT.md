# État réel au 25 novembre 2026

## Vérifications exécutées

- `python3 -m unittest discover -s tests -v` : 11 tests passent, 1 test d'intégration ignoré.
- `python3 -m compileall -q src scripts modal_app.py` : succès.
- `python3 scripts/report.py` : rapport sans chiffres fictifs en l'absence de logs.

Les tests des rollouts utilisent un environnement factice minimal. Il ne remplace
pas TextWorld et ses succès ne sont pas des performances du modèle.

## Blocages observés

- `uv pip install` : crash du composant system-configuration de uv sur ce Mac.
- `python -m pip install textworld ...` : échec de résolution DNS de pypi.org.
- `curl https://pypi.org/...` : même erreur de résolution DNS.
- Les poids Qwen ne sont pas présents localement. Aucun entraînement lancé.
- Modal n'est pas installé. Aucun crédit GPU consommé par cette session.
- La création du deck dans Spaces est refusée (`page_age_restricted`). Le rendu
  fourni est donc un fichier HTML local autonome, sans appel à ce service.

## Non validé

Installation Linux/Docker/Modal, compilation des jeux, oracle, collecte réelle,
tokenizer Qwen réel, fine-tuning, consommation mémoire, temps et coût GPU,
rollouts, amélioration par LoRA, transfert et ablation de l'historique.

## Terminer l'expérience

Suivre README.md, exécuter d'abord le test d'intégration. En cas d'échec, corriger
le pipeline avant d'engager une grande expérience. Après exécution, générer le
rapport et remplacer les diapositives « mesures non disponibles » par des valeurs
provenant des logs. Conserver une copie de cet état pour la traçabilité.

## Présentation et publication

- Diaporama HTML : 16 sections et 16 notes vérifiées par analyse HTML ; JavaScript
  valide avec `node --check`. Vérification visuelle impossible : hôte du navigateur
  indisponible et ouverture du serveur local refusée par le bac à sable.
- Initialisation `.git` dans le workspace refusée (répertoire protégé en lecture).
  Un dépôt de publication distinct est préparé dans `/private/tmp/rl-epita-s9-publish`.
- GitHub inaccessible par DNS (`Could not resolve host: github.com`). Le push reste
  à effectuer ; aucun dépôt distant n'a été vérifié ou modifié.
- Workflow GitHub Actions fourni pour lancer le test d'intégration Linux après
  publication. Il n'a pas tourné et ne télécharge aucun modèle pour le training.
