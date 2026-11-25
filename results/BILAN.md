# Bilan des expériences réelles

## Question et protocole

Nous cherchons à savoir si un SLM peut apprendre à exécuter des quêtes TextWorld
par imitation de démonstrations expertes. Ce projet utilise un environnement RL,
mais entraîne sa politique par **behaviour cloning**, sans optimiser une récompense.

360 jeux sont séparés avant collecte : par niveau, 120 train, 20 validation,
40 test. Une démonstration train avancée est rejetée pour une ambiguïté de noms
dans le parseur, avec trace et rapport. Les 239 jeux train acceptés fournissent
1179 exemples ; les 40 jeux validation, 192. Les 279 démonstrations ont été
rejouées : 1371 transitions observation/action/récompense/observation suivante.
Aucune démonstration du test n'est utilisée pour apprendre.

Deux adaptateurs LoRA sont appris depuis **la même base Qwen2.5-0.5B-Instruct** :
355 exemples simples pour A ; 1179 simples+avancés pour B. Chacun entraîne
1 081 344 paramètres (0,2184 % du modèle adapté), avec loss sur l'action seulement.
Trois époques configurées, graine 42, contexte 1024, LoRA q/v r16 alpha32,
batch 2 et accumulation 8, learning rate 2e-4. Le meilleur checkpoint est choisi
par loss de validation. Le test est ouvert après fixation du protocole.

## Expériences, motivations et observations

1. **Base contre LoRA simple, sur simple.** L'adaptation doit apprendre la forme
   des commandes et le suivi de l'objectif. Base : 0/40 (0.0 %) ; LoRA :
   33/40 (82.5 %), soit 82.5 points de plus.
   Il s'agit d'une amélioration sur ces jeux générés, pas d'un résultat universel.
2. **Transfert vers le niveau 2.** La quête passe de longueur 3 à 7 et de largeur 1
   à 2, avec davantage de pièces et d'objets. LoRA simple réussit
   4/40 (10.0 %). La réussite sur les tâches courtes ne suffit donc
   pas à démontrer une bonne généralisation aux quêtes longues.
3. **Nouvelles démonstrations complexes.** LoRA mixte atteint
   31/40 (77.5 %) sur avancé et 39/40 (97.5 %) sur simple.
   Cette expérience modifie à la fois diversité, quantité de données et nombre de
   mises à jour : on ne peut pas isoler l'effet causal de la seule diversité.
4. **Ablation de prompt, technique avancée.** Avec le même adaptateur A, retirer
   l'historique donne 1/40 (2.5 %) sur simple, contre
   33/40 (82.5 %) avec historique. Le modèle a été entraîné avec
   historique : l'ablation révèle sa sensibilité à cette modification d'entrée,
   sans prouver que toute forme de mémoire bénéficie à tout modèle.
5. **Contrôles de l'environnement.** Oracle : 40/40 (100.0 %) sur simple,
   40/40 (100.0 %) sur avancé. Aléatoire admissible :
   7/40 (17.5 %) et 0/40 (0.0 %). Ils possèdent des
   informations privilégiées absentes des prompts du SLM.

Le taux d’invalidité agrège les commandes de toutes les parties : les échecs
longs y pèsent davantage que les victoires courtes. Le taux de victoire se calcule
par jeu. Ces deux pourcentages n’ont donc pas le même dénominateur.

Le tableau complet, coups moyens, taux de commandes non admissibles, revisites et
IC de Wilson à 95 % est dans [rapport.md](rapport.md). Les 12 conditions du test
représentent 480 épisodes ; les 12 conditions de validation 240, soit 720 au total.
Les IC décrivent l'incertitude sur les jeux, pas la variabilité des réentraînements.
Une seule graine d'entraînement a été testée ; les écarts restent descriptifs.

## Échecs et corrections justifiées

- **Collecte :** le solveur de `advanced-110084` répète une commande ambiguë entre
  `Canadian locker` et `Canadian limited edition locker`. Cette démonstration
  perdante est rejetée, sans retirer de jeu test.
- **Contexte :** deux observations initiales train dépassaient 1024 tokens à cause
  de la bannière ASCII. Après retrait de l'historique ancien, seule la décoration
  et la répétition de l'objectif dans le feedback sont retirées si nécessaire.
  Le texte d'objectif, la description et l'inventaire restent accessibles.
  Les 415 entrées simples sont identiques avant/après la correction ; les 1371
  exemples mixtes train+validation sont désormais encodables.
- **Partie réelle :** sur `easy-30000`, LoRA simple produit `take insect from floor`.
  Le jeu répond `You can't see any such thing.` Le modèle part au sud malgré
  l'échec de prise, puis tente de déposer l'insecte et répète des commandes.
  Bilan : 30 coups, 29 non admissibles, pas de victoire. L'objet est mentionné
  dans l'objectif : cet échec n'est pas une preuve d'objet halluciné.
- **Diagnostic :** le feedback contient un compteur de tours. Il ne doit pas
  entrer dans la signature de revisite. Le diagnostic version2 est recalculé
  depuis les traces, en vérifiant que victoires, coups et invalidité sont inchangés.

Les premières traces perdantes par identifiant sont sélectionnées de façon
systématique dans [ECHECS.md](ECHECS.md), sans choisir uniquement un cas spectaculaire.
Une répétition de description/inventaire/commande peut être légitime ; elle ne
prouve pas à elle seule une boucle sans issue. Le BC expose surtout aux états
experts ; une couverture insuffisante des états après erreur est une explication
plausible, pas une cause identifiée par ces seules observations.

## Temps, vérifications et limites

Entraînement simple : 313,4 secondes, 66 mises à jour. Entraînement mixte : 932,4
secondes, 219 mises à jour, sur T4. Ces durées excluent compilation et évaluation.
Les losses minimales de validation sont 0,08927 et 0,02863 ; leurs jeux de validation
diffèrent, donc ces nombres ne se comparent pas directement.

18 tests réussissent sous Linux, sans test ignoré, dont compilation TextWorld et
partie experte. Les poids sont finis et les empreintes des données correspondent
aux modèles. Les traces et adaptateurs sont conservés dans l'archive, avec SHA256.
Le runner GitHub Actions n'a pas pu démarrer à cause d'une restriction du compte ;
la preuve d'exécution est le journal Linux Modal. Le coût facturé du compte et le
pic de mémoire GPU n'ont pas été mesurés : ne pas confondre un tarif estimé avec
une facture vérifiée.

L'agent reçoit une description et un inventaire à chaque pas, ainsi qu'un objectif
public souvent très explicite. Cela mesure surtout l'exécution de consignes dans
un benchmark contrôlé. L'invalidité est un proxy fondé sur les commandes admissibles,
qui peut compter des synonymes compris par le parseur. Aucune commande générée
n'est remplacée par une commande admissible. Les splits utilisent des jeux distincts,
mais la grammaire commune et les structures proches limitent la portée du transfert.

## Suites possibles, non implémentées

Comparer les données à nombre de tokens et pas d'optimisation égaux ; répéter
plusieurs graines ; collecter des corrections expertes dans les états visités par
l'agent (DAgger) sur train ; comparer d'autres modèles ; tester un objectif plus
court sur un nouveau test réservé. Jericho et ALFWorld ne sont pas implémentés.
