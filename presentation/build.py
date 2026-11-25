"""Construit un diaporama HTML autonome, avec notes orales et impression."""
import argparse
import shutil
from html import escape
from pathlib import Path
import json

SLIDES = [
("Un petit modèle apprend à jouer", "TextWorld · Qwen 0.5B · LoRA", "Observer. Choisir une commande. Accomplir une quête.",
 "0:00–0:40. Notre question est expérimentale : l'imitation de solutions expertes améliore-t-elle une politique sur des jeux nouveaux ? Annoncer d'emblée l'état réel : pipeline écrit, entraînement non exécuté dans la session de préparation. Ne pas annoncer de résultat sans logs."),
("Une partie textuelle", "Exemple illustratif", "Observation : une clé au sol\nCommande : take key\nNouvelle observation : la clé est dans l'inventaire",
 "0:40–1:20. Cet exemple sert à expliquer le format, ce n'est pas une sortie du modèle. TextWorld produit observation, score cumulé et fin. Notre récompense de transition est la différence des scores. Le modèle ne voit que le texte public. Source : Côté et al., https://arxiv.org/abs/1806.11532"),
("Une politique avec mémoire", "π(action | historique, observation)", "État caché : le monde complet\nObservation : le texte accessible\nMémoire : jusqu’à quatre échanges récents",
 "1:20–2:00. Expliquer la partial observability. La description et l'inventaire sont fournis à chaque pas : c'est une aide déclarée du protocole. On retire d'abord les échanges les plus anciens si le contexte dépasse 1024 tokens."),
("L'expert construit les exemples", "Une transition = un exemple", "Jeu train\nObservation publique + historique\nProchaine commande du solveur",
 "2:00–2:45. TextWorld calcule une politique gagnante à partir de l'état symbolique. On exécute cette politique et ne garde que les parties gagnées. Aucune démonstration test n'est produite. Le solveur fournit les étiquettes, il n'entre pas dans les prompts. Source : https://textworld.readthedocs.io/en/stable/textworld.html"),
("L'apprentissage par imitation", "Prédire la commande experte", "Loss = −log P(tokens de l'action | contexte)\nPrompt et padding masqués\nRécompense utilisée pour évaluer",
 "2:45–3:35. Faire le lien avec le TP LunarLander : observation -> action d'un expert. Ici l'action est une séquence de tokens. Les labels −100 ignorent le prompt et le padding. C'est du behaviour cloning, pas une optimisation par PPO. Une baisse de loss ne prouve pas que le modèle gagne."),
("LoRA : une petite correction", "W reste figée", "W adaptée = W + (α/r)BA\nRang r = 16\nAdaptation des projections q et v",
 "3:35–4:25. Expliquer les dimensions de A et B à l'oral. Pour une matrice illustrative 1024×1024, rang 16, on apprend 32768 paramètres plutôt que 1048576. Ce n'est pas le total mesuré de Qwen. LoRA économise surtout gradients et états optimiseur ; la base reste en mémoire. Source : Hu et al., https://arxiv.org/abs/2106.09685"),
("Des jeux séparés avant la collecte", "Par niveau", "120 jeux d'entraînement\n20 jeux de validation\n40 jeux de test réservés",
 "4:25–5:05. Les nombres décrivent le protocole prévu. Toutes les transitions d'un jeu restent dans le même split. Les empreintes vérifient l'intégrité. Des graines différentes ne garantissent pas une structure sémantique totalement nouvelle. Le checkpoint est choisi par loss de validation."),
("L'expérience principale", "Le fine-tuning aide-t-il ?", "Modèle initial\nLoRA sur jeux simples\nMêmes jeux de test, même limite de 30 coups",
 "5:05–5:50. La motivation est d'isoler l'effet de l'adaptation du modèle à la commande textuelle. Génération greedy, pas de correction vers la liste d'actions valides. Ajouter oracle comme contrôle de gagnabilité et aléatoire admissible comme référence privilégiée. Ces deux baselines ne disposent pas des mêmes informations que le LLM."),
("Le transfert vers des quêtes longues", "Niveau 2", "Simple : 3 pièces, quête de 3 actions\nAvancé : 6 pièces, quête de 7 actions\nRéentraînement sur simple + avancé",
 "5:50–6:40. Largeur de quête 1 puis 2 pour introduire des sous-objectifs combinés. Mesurer LoRA easy sur les deux niveaux, puis comparer LoRA mixed sur avancé. Mixed reçoit davantage de données et de mises à jour : un gain ne prouverait pas un effet de la seule complexité. Les longueurs annoncées sont des paramètres de génération à vérifier par les traces oracle."),
("L'ablation de la mémoire", "Même checkpoint, deux prompts", "Jusqu’à 4 échanges récents\nHistorique vide\nComparer victoire et boucles",
 "6:40–7:20. Technique avancée retenue : comparaison de stratégies de prompt. Hypothèse : l'historique aide à garder une progression et évite certaines répétitions. Il peut aussi distraire ou augmenter le coût. Le modèle est entraîné avec historique 4 : historique 0 crée un décalage d'inférence. Aucun résultat de cette comparaison n'est encore disponible."),
("L'évaluation fait jouer l'agent", "La loss ne suffit pas", "Quêtes gagnées + IC 95 %\nCoups sur tous les épisodes et sur les réussites\nActions invalides, boucles, troncatures",
 "7:20–8:10. IC de Wilson sur les jeux. Il ne couvre pas la variation entre réentraînements. Avec 40 jeux, une victoire vaut 2,5 points. Invalidité = absence dans les actions admissibles, avec exceptions look/inventory : des synonymes peuvent être mal comptés. Une revisite peut être utile, donc l'indicateur boucle demande une lecture humaine."),
("Résultats : mesures non disponibles", "État vérifié du projet", "13 tests unitaires réussis\nIntégration TextWorld non exécutée\nAucun entraînement ni taux de victoire mesuré",
 "8:10–9:00. Expliquer le blocage précis : résolution DNS de pypi.org refusée dans l'environnement local, dépendances absentes. Les tests unitaires valident les masques, les métriques et les protections de données ; ils ne remplacent pas un test du modèle. Le rapport sera calculé par scripts/report.py uniquement à partir des logs réels."),
("Comprendre un échec", "Une trace complète par partie", "Commande impossible ?\nSous-objectif oublié ?\nÉtat visité en boucle ?",
 "9:00–9:45. Ce sont des catégories d'analyse prévues, pas des échecs déjà observés. Lire le premier écart et le feedback du jeu. Ne pas appeler toute action invalide hallucination : le modèle peut simplement utiliser un synonyme ou oublier une précondition. Le BC voit les états experts et peut manquer de couverture lorsqu'il s'égare."),
("Ce qu'il reste à mesurer", "Priorité : une exécution réelle", "Valider TextWorld et l'oracle\nEntraîner puis comparer sur test réservé\nConserver aussi les résultats négatifs",
 "9:45–10:35. Modal T4, maximum 30 minutes par appel, aucun retry automatique, un seul conteneur. Ce n'est pas un plafond global de facturation. Vérifier les coûts après chaque phase et arrêter avant le budget utilisateur de 7 euros. Ne pas prétendre que le GPU a tourné. Source tarifaire : https://modal.com/pricing"),
("Ce que l'expérience peut montrer", "Une politique sur un benchmark contrôlé", "L'imitation peut apprendre des commandes\nLa généralisation exige des parties nouvelles\nLes traces expliquent les limites",
 "10:35–11:15. Ces phrases présentent les idées à tester, sans conclure à un gain non mesuré. Extension possible : DAgger pour collecter les actions expertes dans les états visités par l'agent sur train. Non implémenté. Source : Ross et al., https://arxiv.org/abs/1011.0686. Ouvrir les questions."),
("Références", "Sources et code consultables", "Côté et al. · TextWorld, 2018\nHu et al. · LoRA, 2021\nRoss et al. · DAgger, 2011\nQwen2.5 · carte modèle officielle",
 "Sources complètes dans docs/REFERENCES.md. https://arxiv.org/abs/1806.11532 ; https://arxiv.org/abs/2106.09685 ; https://arxiv.org/abs/1011.0686 ; https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct. Jericho et ALFWorld sont des extensions possibles non implémentées.")
]

CSS = '''
*{box-sizing:border-box}html,body{margin:0;background:#101c29;color:#f2f6f8;font-family:Arial,sans-serif}body{overflow:hidden}
.slide{display:none;min-height:100vh;padding:7vh 9vw 10vh;position:relative}.slide.active{display:flex;flex-direction:column;justify-content:center}
.kicker{color:#74dece;font-size:clamp(16px,2vw,28px);margin:0 0 3vh}h1{font-size:clamp(30px,4.8vw,74px);letter-spacing:-.03em;line-height:1.08;max-width:1100px;margin:0 0 6vh}
.body{font-size:clamp(20px,2.7vw,42px);line-height:1.55;white-space:pre-line;margin:0;max-width:1100px}.foot{position:absolute;bottom:4vh;left:9vw;right:9vw;display:flex;justify-content:space-between;font-size:14px;color:#aabdc8}
.chart{display:block;width:100%;max-height:65vh;object-fit:contain}.chart-slide h1{font-size:44px;margin-bottom:12px}.chart-slide .kicker{font-size:22px;margin-bottom:14px}aside{display:none;position:fixed;bottom:7vh;right:2vw;left:2vw;background:#eef5f8;color:#13202c;padding:20px 26px;border:2px solid #74dece;font-size:18px;line-height:1.5;z-index:3;max-height:34vh;overflow:auto}.notes aside{display:block}button{border:0;background:transparent;color:#aabdc8;font-size:20px;cursor:pointer;padding:10px}nav{position:fixed;bottom:0;right:2vw;z-index:5}.sr{position:absolute;width:1px;height:1px;overflow:hidden}
@media print{@page{size:landscape;margin:0}body{overflow:visible;background:#101c29;-webkit-print-color-adjust:exact;print-color-adjust:exact}.slide,.slide.active{display:flex;min-height:100vh;height:100vh;break-after:page;padding:7vh 9vw}aside,nav{display:none!important}h1{font-size:42px}.body{font-size:26px}.kicker{font-size:20px}}
'''
parser = argparse.ArgumentParser()
parser.add_argument("--results", default="artifacts/eval/test")
parser.add_argument("--output", default=str(Path(__file__).parent))
parser.add_argument("--figure", help="Figure de réussite produite à partir des résultats réels")
args = parser.parse_args()
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)
measured = []
for level in ["easy", "advanced"]:
    rows = []
    for name in ["oracle", "random", "base", "lora_easy", "lora_easy_h0", "lora_mixed"]:
        path = Path(args.results) / f"{name}_{level}" / "summary.json"
        if not path.exists():
            continue
        summary = json.loads(path.read_text())
        if not summary.get("complete"):
            continue
        m = summary["metrics"]
        rows.append(f"{name} : {m['success_rate']:.0%} gagnés, {m['mean_steps_all']:.1f} coups")
    if rows:
        measured.append((f"Résultats mesurés : {level}", "Réussite et coups moyens sur tous les épisodes",
            "\n".join(rows), "Mesures issues de summary.json. Nombre de jeux, IC Wilson 95 %, invalidité et boucles dans resultats.md. Une graine de fine-tuning. Baselines oracle et random : information privilégiée. Une ligne absente désigne une condition non terminée."))
if measured:
    if args.figure:
        figure = Path(args.figure)
        if not figure.is_file():
            raise FileNotFoundError(figure)
        target = output / figure.name
        if figure.resolve() != target.resolve():
            shutil.copy2(figure, target)
        SLIDES[11:12] = [("Réussite sur des jeux non vus", "Barres : victoire ; traits : IC de Wilson à 95 %",
            "figure:" + target.name,
            "Résultats issus des rollouts complets. Aléatoire et oracle disposent d'informations privilégiées. Les nombres au-dessus des barres indiquent victoires / jeux. Tous les coups, non-admissibles et boucles sont dans le rapport. Une seule graine de fine-tuning : les IC reflètent la variation des jeux, pas celle des entraînements.")]
    else:
        SLIDES[11:12] = measured
    SLIDES = [(t,k,b,n) for t,k,b,n in SLIDES if t != "Ce qu'il reste à mesurer"]
    SLIDES[0] = (SLIDES[0][0], SLIDES[0][1], SLIDES[0][2],
        "0:00–0:40. Présenter la question et le protocole. Les diapositives de résultats ne contiennent que les conditions terminées. Vérifier que les douze conditions sont présentes avant d'annoncer une comparaison complète.")
parts = []
for i, (title, kicker, body, notes) in enumerate(SLIDES):
    content = (f'<img class="chart" src="{escape(body[7:])}" alt="Réussite par agent et niveau, intervalles de Wilson 95 %">'
               if body.startswith("figure:") else f'<p class="body">{escape(body)}</p>')
    chart_class = " chart-slide" if body.startswith("figure:") else ""
    parts.append(f'<section class="slide{chart_class}{" active" if i == 0 else ""}" aria-label="Diapositive {i+1}"><p class="kicker">{escape(kicker)}</p><h1>{escape(title)}</h1>{content}<div class="foot"><span>TextWorld · Projet RL EPITA</span><span>{i+1:02} / {len(SLIDES)}</span></div><aside>{escape(notes)}</aside></section>')
script = '''let current=0;const slides=[...document.querySelectorAll('.slide')];function show(i){current=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,j)=>s.classList.toggle('active',j===current));location.hash=current+1;}function move(d){show(current+d)}function notes(){document.body.classList.toggle('notes')}function full(){if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.()}document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();move(1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='n')notes();if(e.key.toLowerCase()==='f')full()});show((parseInt(location.hash.slice(1))||1)-1);'''
html = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TextWorld et LoRA — Projet RL</title><style>'+CSS+'</style></head><body>'+''.join(parts)+'<nav aria-label="Navigation"><button onclick="move(-1)" aria-label="Précédente">←</button><button onclick="move(1)" aria-label="Suivante">→</button><button onclick="notes()">Notes</button><button onclick="full()">Plein écran</button></nav><script>'+script+'</script></body></html>'
(output / 'index.html').write_text(html, encoding='utf-8')
(output / 'notes.md').write_text('\n\n'.join(f'## {i+1}. {t}\n\n{n}' for i,(t,k,b,n) in enumerate(SLIDES)), encoding='utf-8')
print(f'{len(SLIDES)} diapositives générées')
