# Un petit modèle apprend à jouer à TextWorld

Projet étudiant de reinforcement learning et d'apprentissage par imitation.
**Question : fine-tuner un modèle de 0,5 milliard de paramètres améliore-t-il sa
capacité à accomplir une quête textuelle sur des jeux jamais vus ?**

## État réel du rendu

L'intégration Linux est validée : **14 tests réussis**, dont la compilation d'un
vrai jeu TextWorld et sa résolution par l'oracle. Le tokenizer Qwen réel et le
masquage de la loss ont aussi été contrôlés. La génération des jeux et les
expériences Modal sont en cours. Les performances seront publiées uniquement
après récupération des rollouts complets. Voir [l'état des vérifications](results/STATUT.md).

## Lire et présenter

- [Présentation hors ligne](presentation/index.html) : ouvrir dans un navigateur,
  flèches pour avancer, `N` pour les notes, `F` pour le plein écran. Impression PDF
  possible via le navigateur. Les diapositives de résultats signalent les mesures absentes.
- [Comprendre le projet](docs/COMPRENDRE.md) : notions, loss et LoRA expliquées.
- [Protocole expérimental](docs/EXPERIENCES.md) : hypothèses, comparaisons et biais.
- [Préparer les questions](docs/ORAL.md) : réponses, liens avec le cours et démonstration.
- [Références](docs/REFERENCES.md) : sources primaires et documentation.

## Installation conseillée : Linux, Python 3.11

TextWorld compile des jeux via Inform 7. Linux évite les difficultés des binaires
sur Apple Silicon. Il faut un accès Internet pour les paquets et les poids publics.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[cloud]'
python -m unittest discover -s tests -v
```

Docker, pour tester l'environnement sans modifier votre Python :

```bash
docker build -t textgames .
docker run --rm textgames
# Pour le GPU local : installer NVIDIA Container Toolkit, puis
# docker run --gpus all -it -v "$PWD/artifacts:/project/artifacts" textgames bash
```

Le test d'intégration doit PASSER, sans « skipped », avant les grandes expériences.
Les versions principales sont fixées dans `pyproject.toml`. Les versions réellement
utilisées et la révision du modèle sont consignées dans `training.json` après training.
Les dépendances transitives et l'image système ne sont pas verrouillées par digest.

## Exécution automatique de tout le protocole

Après installation des dépendances, une seule commande enchaîne le test réel,
la collecte, les deux fine-tunings, les 24 évaluations (validation puis test),
le rapport et les diapositives contenant les mesures disponibles :

```bash
python scripts/finish_project.py
# Ou sur Modal, avec GPU T4 et un timeout global de deux heures pour cet appel :
modal run modal_app.py --phase all
```

Les livrables calculés arrivent dans `artifacts/delivery/`. Les journaux détaillés
sont dans `artifacts/execution/`. En cas d'échec, l'exécution s'arrête et annonce
l'étape en échec ; aucun statut « terminé » n'est produit. Une relance reprend
les évaluations dont la provenance correspond exactement aux jeux et aux poids.
Les modèles ayant un entraînement complet et les mêmes données sont réutilisés.
Les fine-tunings interrompus sont recommencés. Ne pas lancer plusieurs commandes
Modal simultanément ni relancer sans consulter le solde restant.

La phase `all` conserve une T4 pendant toute sa durée (y compris génération et
tests), contrairement aux phases séparées plus économes. Le timeout de deux
heures concerne un appel, pas un plafond de dépenses pour le compte. La durée
réelle de ce protocole n'a pas pu être mesurée dans cette session.

## Exécution locale complète

```bash
# 1. Génération des jeux compilés et démonstrations expertes
python scripts/run_experiments.py --phase prepare
# 2. LoRA easy et LoRA mixed, sélection des checkpoints par loss de validation
python scripts/run_experiments.py --phase train
# 3. Analyse sur validation, avant toute ouverture du test final
python scripts/run_experiments.py --phase validation
# 4. Test final une fois le protocole figé
python scripts/run_experiments.py --phase test
# 5. Tableau calculé à partir des logs
python scripts/report.py
```

Premier essai : `--phase prepare --scale 0.05`, puis entraînement d'un seul modèle
avec `python -m textgame.train --max-steps 2 --output artifacts/smoke_adapter`.
Ce mini-essai vérifie l'exécution, il ne mesure pas une performance exploitable.
Faire ce smoke test dans un répertoire séparé (`--root artifacts_smoke`) ou supprimer
ses artefacts avant le protocole complet. Ne pas mélanger des manifestes de tailles différentes.

## Modal et budget

Installer `modal`, puis utiliser l'authentification interactive `modal setup` avec
votre compte. Aucun secret ne doit être ajouté au dépôt. Le secret partagé dans la
conversation est à révoquer et remplacer.

```bash
modal run modal_app.py --phase prepare
modal run modal_app.py --phase train --experiment lora_easy
modal run modal_app.py --phase train --experiment lora_mixed
# Répéter par agent et niveau pour garder des appels courts :
modal run modal_app.py --phase validation --experiment lora_easy --level easy
modal run modal_app.py --phase test --experiment lora_easy --level easy
modal volume get textgames-student /artifacts ./artifacts
python scripts/report.py
```

Pour le tableau complet, évaluer chacun des six agents (random, oracle, base,
lora_easy, lora_easy_h0, lora_mixed) sur chacun des deux niveaux. Les options
`--experiment` et `--level` existent aussi pour le script local. Les commandes
Modal ci-dessus ne lancent volontairement qu'une condition d'évaluation à titre
d'exemple ; elles ne suffisent pas à produire le tableau complet.

Les appels GPU emploient une T4, un seul conteneur, zéro retry et un timeout de
30 minutes par appel. Le tarif consulté le 25/11/2026 est de 0,000164 USD/s pour
la T4, soit environ 0,59 USD/h, hors CPU, RAM et stockage. Ce timeout limite une
exécution, **il ne constitue pas un plafond global de facturation**. Vérifier le
solde et le coût observé après chaque phase, arrêter avant 7 euros. Les durées
réelles ne sont pas encore mesurées. Un appel peut expirer avant sa fin.
Les jeux compilés sont produits dans l'image Linux CPU, l'entraînement et
l'inférence tournent sur GPU. Le volume conserve les fichiers terminés.

## Organisation du code

| Fichier | Responsabilité |
|---|---|
| `games.py` | Génération, splits, contrôle des empreintes, ouverture TextWorld |
| `data.py` | Collecte oracle gagnante, sans démonstrations du test |
| `common.py` | Prompts et observations publiques, entrées/sorties JSON |
| `tokenization.py` | Loss sur action uniquement, retrait de l'historique trop long |
| `train.py` | LoRA et sauvegarde du meilleur checkpoint de validation |
| `agents.py` | Génération libre d'une commande et baseline aléatoire |
| `evaluate.py` | Parties complètes, IC de Wilson, invalidité et boucles |
| `scripts/report.py` | Tableau à partir des résultats réellement sauvegardés |

Les modules se trouvent dans `src/textgame/`. Les entraînements utilisent des
commandes anglaises car TextWorld produit ici des jeux en anglais. La documentation
et l'oral sont en français.

## Démonstration à la soutenance

```bash
python scripts/play.py artifacts/games/easy/test/30000.z8 --adapter artifacts/lora_easy
```

Si aucun entraînement n'a pu être terminé, montrer le code et expliquer le blocage.
Préférer une trace réelle enregistrée à une démonstration improvisée. Ne jamais
faire passer une trace inventée pour une partie du modèle.
