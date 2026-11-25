# Soutenance : comprendre avant de réciter

Durée visée : 12 minutes, puis questions. La présentation HTML possède des notes
par diapositive (`N`). Répartir les parties entre membres et permettre à chacun
d'expliquer le code du prompt, le masque et une trace d'échec.

## Questions sur ce projet

**Est-ce du reinforcement learning ?** L'environnement est séquentiel, avec états,
actions et récompenses. L'algorithme d'entraînement est du behaviour cloning,
donc de l'imitation supervisée. Pas de mise à jour par récompense dans notre LoRA.

**Pourquoi Qwen 0.5B ?** C'est un décodeur instruct génératif assez petit pour
expérimenter avec un faible budget. La qualité réelle doit être mesurée.

**Pourquoi pas simplement donner le walkthrough au prompt ?** Cela fournirait la
solution au lieu de mesurer une politique apprenant à agir à partir d'observations.

**Pourquoi LoRA ?** Réduire les paramètres entraînables et les états d'optimiseur.
La base est figée, les petites matrices reçoivent les gradients.

**Pourquoi certaines actions valides échouent ?** Une commande peut être comprise
mais avoir une précondition absente. Elle peut aussi être valide et inutile.
Validité, progrès et réussite sont trois concepts différents.

**Pourquoi l'historique peut aider ?** Pour mémoriser les actions précédentes et
les informations qui ne sont plus visibles. Son coût est un contexte plus long.
Notre inventaire explicite atténue déjà une partie de la difficulté de mémoire.

**Peut-on affirmer que l'agent raisonne ?** Une hausse de victoire montre une
meilleure politique sur ce benchmark, pas une preuve de raisonnement général.

**Quelle limite majeure du BC ?** L'entraînement voit les états experts, mais
l'agent s'égare et rencontre d'autres états. DAgger traiterait mieux leur couverture.

**Pourquoi pas seulement l'accuracy sur les actions ?** Plusieurs commandes
peuvent mener à la victoire. Une égalité exacte avec une commande experte est
insuffisante ; l'épisode complet mesure l'objectif réel.

## Liens avec les notions annoncées par le professeur

- Retour : somme des récompenses futures pondérées par γ. Ici, le score final
  représente les sous-objectifs accomplis ; la victoire est notre mesure principale.
- ε-greedy : action aléatoire avec probabilité ε, sinon meilleure action estimée.
  Ce n'est pas notre décodage greedy, qui choisit chaque token le plus probable.
- Q-learning tabulaire : Q(s,a) ← Q(s,a)+α[r+γ max_a'Q(s',a')−Q(s,a)].
  L'espace textuel rend le tableau difficile à couvrir.
- DQN (Mnih et al.) : approximation de Q par réseau, replay buffer pour réutiliser
  les transitions et réduire leur corrélation, réseau cible pour stabiliser les cibles.
- DDPG (Lillicrap et al.) : acteur déterministe et critique Q pour actions continues.
  Nos commandes sont discrètes et séquentielles, DDPG n'est pas directement adapté.
- Exploration / exploitation : chercher des informations nouvelles ou utiliser
  ce qu'on croit déjà efficace. L'expert évite ici le coût d'exploration du training.
- Entropie : −Σp log p, mesure de dispersion d'une politique. Une régularisation
  entropique favorise des politiques moins concentrées. Nous n'en ajoutons pas.
- Récompense extrinsèque : réussite de quête donnée par le jeu. Intrinsèque : signal
  auxiliaire de nouveauté/curiosité. Aucune curiosité n'est implémentée ici.
- Domain randomization : varier les environnements pour apprendre des invariances.
  Générer des cartes et noms différents s'en rapproche, sans garantir le transfert
  vers Zork ou ALFWorld dont les règles et le langage changent davantage.

Ces fiches ne remplacent pas la lecture des articles demandés en cours. Savoir
expliquer l'intuition, la règle de mise à jour et les limites est plus utile que
mémoriser une formule isolée.

## Démonstration et réponses honnêtes

1. Montrer une observation publique et la commande proposée.
2. Expliquer l'action réellement exécutée et la récompense de transition.
3. Relire une réussite ET un échec issus des logs, si disponibles.
4. Afficher un tableau de résultats calculé automatiquement, si disponible.

État actuel : aucun entraînement exécuté, aucun résultat de jeu. Dire explicitement
« nous avons construit le pipeline, mais son exécution reste à valider » si ce
blocage persiste au moment de l'oral. Ne pas dire « le modèle gagne » sans trace.
