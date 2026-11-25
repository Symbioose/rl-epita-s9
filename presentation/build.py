"""Soutenance visuelle : 10 slides, illustrations vectorielles et données réelles."""
import argparse
import base64
import json
from html import escape as esc
from pathlib import Path

BG = '#F6F3EC'
INK = '#142939'
BLUE = '#365CF5'
ORANGE = '#E77343'
GREEN = '#087B68'
MUTED = '#60717C'
PALE = '#E6E9F5'
RED = '#B84340'


def text(x, y, content, size=26, fill=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(str(content))}</text>'


def lines(x, y, content, size=26, fill=INK, gap=None, weight=400):
    return ''.join(text(x, y+i*(gap or size*1.4), line, size, fill, weight) for i,line in enumerate(content))


def rect(x,y,w,h,fill=PALE,rx=12,stroke='none',sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1,y1,x2,y2,color=INK,width=3,dash=''):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def arrow(x1,y1,x2,y2,color=BLUE,width=4):
    # Only horizontal / vertical arrows, to keep flow directions easy to read.
    if x2>x1: tip=f'{x2-11},{y2-7} {x2},{y2} {x2-11},{y2+7}'
    elif x2<x1: tip=f'{x2+11},{y2-7} {x2},{y2} {x2+11},{y2+7}'
    elif y2>y1: tip=f'{x2-7},{y2-11} {x2},{y2} {x2+7},{y2-11}'
    else: tip=f'{x2-7},{y2+11} {x2},{y2} {x2+7},{y2+11}'
    return line(x1,y1,x2,y2,color,width)+f'<polyline points="{tip}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def circle(x,y,r,fill=BLUE,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'


def chest(x,y,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})">'+rect(0,25,140,100,'#D6AA76',6,INK,3)+rect(0,0,140,46,'#E5C49D',18,INK,3)+rect(61,36,20,35,ORANGE,3,INK,2)+line(12,88,128,88,'#A47C51',2)+'</g>'


def person(x,y,color=BLUE):
    return circle(x,y,18,color)+f'<path d="M{x-28},{y+65} Q{x-28},{y+25} {x},{y+25} Q{x+28},{y+25} {x+28},{y+65}Z" fill="{color}"/>'


def room_scene(x=65,y=185):
    # Schematic of the observed Cubicle -> Kitchenette transition, not the entire map.
    s=rect(x,y,400,260,'#ECE7DC',0,INK,2)+rect(x+555,y,480,260,'#E7EDE8',0,INK,2)
    s+=line(x+400,y+100,x+555,y+100,INK,2)+line(x+400,y+160,x+555,y+160,INK,2)
    s+=text(x+24,y+42,'CUBICLE',22,INK,700)+text(x+579,y+42,'KITCHENETTE',22,INK,700)
    s+=person(x+170,y+120)+chest(x+820,y+85,.85)
    s+=arrow(x+235,y+132,x+665,y+132,BLUE,5)+text(x+438,y+88,'est',24,BLUE,600)
    s+=circle(x+864,y+161,9,ORANGE)+text(x+790,y+233,'type B locker',22)
    return s


def shell(title,n,dark=False):
    bg=INK if dark else BG
    ink=BG if dark else INK
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><rect width="1280" height="720" fill="{bg}"/>'
    s+=text(64,88,title,48,ink,700)
    s+=text(64,684,'TextWorld / Qwen 0.5B / LoRA',16,'#ADC2CC' if dark else MUTED)
    s+=text(1215,684,f'{n:02}',18,'#ADC2CC' if dark else MUTED,anchor='end')
    return s


def raster(path,x,y,w,h):
    uri='data:image/png;base64,'+base64.b64encode(Path(path).read_bytes()).decode()
    return f'<image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}"/>'


def plots(metrics, folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':17,'text.color':INK,
        'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':MUTED,'axes.edgecolor':'#A8B2B6',
        'figure.facecolor':BG,'axes.facecolor':BG})
    names=['random','base','lora_easy','lora_mixed','oracle']
    labels=['Hasard*','Initial','LoRA simple','LoRA mixte','Oracle*']
    fig,axs=plt.subplots(1,2,figsize=(12.2,4.7),sharey=True,layout='constrained')
    for ax,level in zip(axs,['easy','advanced']):
        for i,name in enumerate(names):
            m=metrics[f'test/{name}_{level}'];p=m['success_rate'];lo,hi=m['success_ci95']
            color=ORANGE if name=='lora_mixed' else BLUE if name=='lora_easy' else '#A7B4BA'
            ax.bar(i,p*100,color=color,width=.62)
            ax.errorbar(i,p*100,yerr=[[100*(p-lo)],[100*(hi-p)]],fmt='none',ecolor=INK,capsize=4,lw=1.6)
            ax.text(i,100*hi+3,f"{m['successes']}/40",ha='center',fontsize=17,fontweight='bold')
        ax.set_ylim(0,119);ax.set_yticks([0,25,50,75,100]);ax.set_xticks(range(5),labels,rotation=20,ha='right')
        ax.set_title('Jeux simples' if level=='easy' else 'Jeux avancés',fontsize=23,fontweight='bold',pad=18)
        ax.spines[['top','right']].set_visible(False);ax.tick_params(length=0,pad=8)
        ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
    axs[0].set_ylabel('Quêtes réussies (%)')
    fig.savefig(folder/'scores.png',dpi=180);fig.savefig(folder/'scores.pdf');plt.close(fig)


def main(results,output,figure=None):
    out=Path(output);assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
    root=Path(results)
    metrics={}
    for level in ['easy','advanced']:
        for agent in ['random','base','lora_easy','lora_easy_h0','lora_mixed','oracle']:
            p=root/f'{agent}_{level}'/'summary.json'
            s=json.loads(p.read_text())
            if not s.get('complete') or s['metrics']['n_games']!=40:raise ValueError(f'Résultat incomplet : {p}')
            metrics[f'test/{agent}_{level}']=s['metrics']
    plots(metrics,assets)
    slides=[]
    asset_prefix="slide"
    def add(title,body,notes,dark=False):
        n=len(slides)+1;svg=shell(title,n,dark)+body+'</svg>'
        name=f'{asset_prefix}-{n:02}.svg';(assets/name).write_text(svg)
        slides.append((title,name,notes))
    def count(agent,level):return metrics[f'test/{agent}_{level}']['successes']

    b=lines(64,196,['Un petit modèle peut-il','apprendre à jouer ?'],62,BG,78,700)
    b+=text(68,410,'Nous lui apprenons à suivre des quêtes textuelles.',26,'#CAD8DB')
    b+=text(68,522,'0,5 milliard',56,'#9DAFFC',700)+text(72,564,'de paramètres dans le modèle initial',22,'#CAD8DB')
    b+=rect(835,174,364,394,'#223C4D',24)
    b+=text(875,227,'UNE VRAIE PARTIE',20,'#A8C3CE',700)+chest(935,274,1.1)
    b+=lines(875,468,['> open type B locker','> take fly larva...'],22,BG,37)
    b+=text(875,565,'Quête accomplie.',25,'#8DE0C4',700)
    add('APPRENDRE À JOUER PAR LE TEXTE',b,'''Durée : 45 secondes.
MONTRER : le coffre et les commandes à droite.
DIRE : notre joueur est un petit modèle génératif Qwen2.5-0.5B-Instruct. Il lit du texte et répond par une commande. La question est de savoir si l’imitation d’un solveur améliore ses parties sur de nouveaux jeux.
TRANSITION : voici d’abord une partie réelle, avant de parler de réseaux de neurones.''',True)

    b=room_scene()+text(65,149,"Objectif : récupérer la larve dans le casier de la kitchenette.",24,MUTED)
    cmds=['go east','open type B locker','take fly larva from type B locker']
    for i,c in enumerate(cmds):
        xx=[65,420,775][i];b+=circle(xx+18,519,18,BLUE)+text(xx+18,526,i+1,20,'white',700,'middle')
        # Last command wraps intentionally over two lines.
        b+=lines(xx,568,[c] if i<2 else ['take fly larva','from type B locker'],23,INK,30,600)
    b+=text(65,643,'3 commandes, victoire. Schéma d’une trace réelle : easy-30001.',20,GREEN,600)
    add('Une quête, trois commandes',b,'''Durée : 75 secondes.
MONTRER : le joueur dans Cubicle, le déplacement vers Kitchenette, puis le coffre.
DIRE : dans cette partie du test, LoRA simple va à l’est, ouvre le type B locker puis prend la fly larva. Les noms et les commandes viennent de la trace easy-30001. Ce dessin représente les deux pièces observées, sans prétendre montrer toute la carte. Le texte décrit d’abord un coffre fermé, puis son contenu après ouverture.
La récompense est la différence entre scores successifs : 0, 0, puis 1. La victoire est vraie après la troisième commande. L’état complet est caché ; l’objectif, la description et l’inventaire sont fournis.
TRANSITION : comment apprendre à choisir ces commandes ?''')

    b=text(65,174,'APPRENTISSAGE',20,MUTED,700)
    cols=[75,475,875]
    for x,title,subtitle,color in zip(cols,['Solveur TextWorld','Démonstrations','Adaptateur LoRA'],['joue les jeux train','contexte + commande','apprend par imitation'],[GREEN,BLUE,ORANGE]):
        b+=circle(x+110,275,66,color)+text(x+110,291,['1','2','3'][cols.index(x)],46,'white',700,'middle')
        b+=text(x+110,388,title,27,INK,700,'middle')+text(x+110,430,subtitle,22,MUTED,anchor='middle')
    b+=arrow(270,275,485,275)+arrow(670,275,885,275)
    b+=line(65,478,1210,478,'#CBD0CB',2)+text(65,527,'ÉVALUATION',20,MUTED,700)
    b+=text(285,537,'Jeux jamais vus',28,INK,700)+arrow(510,528,675,528)+text(710,537,'Le modèle joue seul',30,BLUE,700)
    b+=text(285,598,'L’expert fournit les réponses pendant la collecte, jamais pendant le test.',23)
    add('L’expert enseigne, puis le modèle joue seul',b,'''Durée : 75 secondes.
MONTRER : suivre le trajet du solveur aux exemples, puis à LoRA ; descendre ensuite à la ligne d’évaluation.
DIRE : le solveur a accès à l’état symbolique pour trouver une bonne action. On exécute ses commandes et on garde les parties gagnantes. Le modèle reçoit uniquement les observations publiques et l’historique. Le walkthrough ne figure pas dans ses entrées.
C’est du behaviour cloning, comme le TP LunarLander : apprendre observation vers action à partir d’un expert. Ici une action est une suite de tokens. Nous utilisons un environnement RL, mais pas une optimisation par PPO ou Q-learning.
TRANSITION : pour mesurer un apprentissage réel, les jeux du test doivent rester séparés.''')

    b=text(66,175,'360 JEUX GÉNÉRÉS, SÉPARÉS AVANT LA COLLECTE',22,MUTED,700)
    widths=[720,120,240];xs=[65,785,905]
    for x,w,c,label in zip(xs,widths,[BLUE,ORANGE,GREEN],['240 train','40 val.','80 test']):
        b+=rect(x,220,w,75,c,0)+text(x+w/2,267,label,26,'white',700,'middle')
    b+=text(65,343,'PAR NIVEAU : 120 TRAIN / 20 VALIDATION / 40 TEST',20,MUTED)
    b+=text(65,429,'SIMPLE',24,BLUE,700)+text(650,429,'AVANCÉ',24,ORANGE,700)
    for i in range(3):b+=rect(65+i*102,461,75,63,'#DCE1F8',0,BLUE,2)
    for i in range(6):b+=rect(650+i*85,461,62,63,'#F5D9C9',0,ORANGE,2)
    b+=text(65,571,'3 pièces · longueur cible 3',25)+text(650,571,'6 pièces · longueur cible 7',25)
    b+=text(65,626,'Après filtrage : 239 jeux train gagnants, 1179 exemples mixtes.',22,GREEN,600)
    add('Des jeux nouveaux pour juger le modèle',b,'''Durée : 70 secondes.
MONTRER : la bande bleue train, orange validation et verte test, puis les deux tailles d’environnement.
DIRE : les nombres de la bande additionnent les deux niveaux. Les graines et empreintes sont distinctes. Toutes les transitions d’un jeu restent dans le même split. La validation sert à choisir le checkpoint ; le test mesure les performances finales.
Au niveau avancé, la largeur de quête passe aussi de 1 à 2, avec des sous-objectifs combinés. Les longueurs 3 et 7 sont des paramètres cibles ; les solutions effectives peuvent être plus courtes.
Une démonstration train avancée est rejetée : ambiguïté entre Canadian locker et Canadian limited edition locker. Le rejet et sa trace sont archivés ; aucun jeu test n’est retiré. On obtient 355 exemples simples ou 1179 mixtes.
TRANSITION : sur ces exemples, quelle partie du texte doit-on apprendre à produire ?''')

    b=text(65,178,'UN EXEMPLE D’ENTRAÎNEMENT',21,MUTED,700)
    b+=rect(65,217,1150,228,'#E7E7E2',16)
    b+=text(95,268,'Contexte fourni au modèle',25,MUTED,700)
    b+=lines(95,316,['Objectif + description + inventaire','Historique des dernières commandes'],27,INK,43)
    b+=rect(670,287,510,110,BLUE,10)+text(695,333,'Commande attendue',20,'#CAD6FF',700)+text(695,373,'open type B locker',31,'white',700)
    b+=line(75,484,620,484,MUTED,2)+line(675,484,1200,484,BLUE,4)
    b+=text(340,529,'Prompt masqué',27,MUTED,700,'middle')+text(935,529,'Loss sur l’action',30,BLUE,700,'middle')
    b+=text(935,576,'− log P(commande | contexte)',26,BLUE,anchor='middle')
    b+=text(65,630,'Le modèle apprend à produire une commande, puis on mesure une partie entière.',23)
    add('Apprendre la commande, token par token',b,'''Durée : 75 secondes.
MONTRER : le contexte gris et la commande bleue. Pointer les deux traits en dessous.
DIRE : le modèle apprend à rendre probable la commande experte, token par token, avec les tokens de fin de message. On masque le prompt et le padding avec des labels −100 : leur texte ne contribue pas à la cross-entropy. Le contexte sert à conditionner la réponse, sans devenir la cible à recopier.
À l’entraînement, il voit les tokens experts précédents, c’est le teacher forcing. En partie, il reçoit ses propres actions précédentes et leurs conséquences. Une petite erreur peut l’amener dans un état rarement vu pendant l’apprentissage : la loss seule ne mesure donc pas la capacité à gagner.
TRANSITION : on peut adapter Qwen sans réentraîner tous ses poids.''')

    b=text(65,174,'W ADAPTÉE = W + (α/r) BA',30,INK,700)
    # Matrices: a deliberately schematic shape, not actual Qwen dimensions.
    for row in range(7):
        for col in range(9):b+=rect(80+col*29,223+row*29,24,24,'#C9D0D5' if (row+col)%3 else '#AAB7BF',1)
    b+=text(205,486,'Base figée W',27,INK,700,'middle')+text(205,527,'Aucun gradient sur W',21,MUTED,anchor='middle')
    b+=text(407,355,'+',60,MUTED,600)
    for row in range(7):
        for col in range(2):b+=rect(520+col*29,223+row*29,24,24,ORANGE,1)
    for row in range(2):
        for col in range(9):b+=rect(645+col*29,295+row*29,24,24,BLUE,1)
    b+=text(602,344,'×',38,MUTED,600)+text(554,486,'B',29,ORANGE,700,'middle')+text(769,486,'A',29,BLUE,700,'middle')
    b+=text(1090,287,'0,218 %',52,BLUE,700,'middle')+lines(985,337,['des paramètres','sont entraînés'],23,INK,34)
    b+=text(520,556,'1,08 M de paramètres · rang 16 · projections q et v',24)
    b+=text(65,626,'Deux adaptateurs depuis la même base : simple (5 min 13 s), mixte (15 min 32 s).',23)
    add('LoRA apprend une petite correction',b,'''Durée : 80 secondes.
MONTRER : la grande matrice grise W, puis les deux matrices fines A et B.
DIRE : LoRA ajoute une correction de faible rang à des poids figés. Le dessin illustre le principe, pas les dimensions exactes de Qwen. Pour une matrice sortie × entrée, B est sortie × r et A est r × entrée. On apprend r(sortie+entrée) paramètres au lieu de sortie×entrée.
Ici 1 081 344 paramètres reçoivent les gradients, soit 0,2184 % du modèle adapté. Nous adaptons q_proj et v_proj avec r16, alpha32. La base reste en mémoire ; ce n’est pas de la QLoRA.
Les deux adaptateurs repartent du même Qwen initial. Le simple utilise 355 exemples, le mixte 1179. Le mixte a davantage de données et de mises à jour : le comparer ne permet pas d’isoler la seule diversité. Temps réels du fine-tuning, hors évaluations.
TRANSITION : est-ce que cette adaptation change les parties sur les jeux non vus ?''')

    b=raster(assets/'scores.png',52,149,1176,442)
    b+=text(66,622,'40 jeux par niveau · intervalles de Wilson à 95 % · * information privilégiée',21,MUTED)
    add('L’adaptation aide, le transfert reste difficile',b,'''Durée : 100 secondes.
MONTRER : commencer par les barres Initial et LoRA simple à gauche. Comparer ensuite LoRA simple et LoRA mixte à droite.
DIRE : motivation 1, le fine-tuning aide-t-il ? Le modèle initial gagne 0/40, le simple 33/40 sur les quêtes simples. Motivation 2, ce modèle transfère-t-il ? Sur avancé, il tombe à 4/40. Motivation 3, de nouvelles démonstrations complexes aident-elles ? Le mixte atteint 31/40 sur avancé et 39/40 sur simple.
Les traits donnent les IC de Wilson à 95 % sur les jeux. Ils ne mesurent pas la variabilité entre réentraînements : nous n’avons qu’une graine. Le hasard choisit parmi les commandes admissibles, l’oracle reçoit un plan ; ils ont des informations privilégiées. Le SLM génère librement, sans correction vers la liste valide.
Les nombres viennent des rollouts sauvegardés. Les coups, invalidité et revisites sont en annexe et dans le rapport.
TRANSITION : une dernière expérience retire uniquement l’historique au même adaptateur.''')

    a=count('lora_easy','easy');z=count('lora_easy_h0','easy')
    b=text(65,174,'MÊME ADAPTATEUR SIMPLE, MÊMES 40 JEUX SIMPLES',22,MUTED,700)
    b+=text(65,280,'Avec historique',29,INK,700)+text(65,328,'jusqu’à 4 échanges',23,MUTED)
    b+=text(65,453,'Historique retiré',29,INK,700)+text(65,501,'aucun échange précédent',23,MUTED)
    for yy,val,color in [(247,a,BLUE),(420,z,ORANGE)]:
        b+=rect(430,yy,650,82,'#E3E5E1',0)+rect(430,yy,650*val/40,82,color,0)
        b+=text(1130,yy+55,f'{val}/40',39,color,700,'middle')
    b+=text(65,605,'Le modèle devient très sensible au retrait de son contexte d’entraînement.',25)
    add('Retirer l’historique fait chuter la réussite',b,'''Durée : 70 secondes.
MONTRER : les deux barres 33/40 et 1/40.
DIRE : cette ablation compare deux stratégies de prompt, notre technique avancée. Le checkpoint, les jeux et le décodage restent les mêmes. On retire les échanges précédents, en gardant observation, objectif, description et inventaire actuels.
Motivation : tester l’utilité de la mémoire récente. L’écart est grand, mais le modèle a été entraîné avec historique : le retirer crée un décalage d’entrée. Cela prouve la sensibilité de cet adaptateur, pas l’utilité universelle de toute mémoire. Nous n’avons pas entraîné un second modèle sans historique.
Sur avancé, le même modèle passe de 4/40 à 0/40. Le tableau complet reste en annexe.
TRANSITION : regardons maintenant comment une erreur peut s’accumuler.''')

    b=text(65,165,'TRACE RÉELLE : LoRA simple, easy-30000',21,MUTED,700)
    steps=[('01','Prise ratée',['take insect from floor'],RED),('02','Départ sans l’objet',['go south'],BLUE),('03','Dépôt impossible',['put insect on mantle'],RED)]
    for i,(n,title,cmd,c) in enumerate(steps):
        x=65+i*407;b+=circle(x+28,246,27,c)+text(x+28,255,n,22,'white',700,'middle')
        b+=text(x,328,title,28,INK,700)+text(x,379,cmd[0],22,c,600)
        if i<2:b+=arrow(x+70,246,x+365,246,'#9AA8AF',3)
    b+=rect(65,423,1150,69,'#F2DED5',8)+text(92,467,'Le jeu avait répondu : “You can’t see any such thing.”',27,RED,600)
    b+=text(65,568,'30 coups',50,INK,700)+text(450,568,'29 non admissibles',43,RED,700)
    b+=text(65,625,'Le modèle continue le plan et répète des commandes malgré l’échec initial.',24)
    add('Une action ratée peut bloquer toute la quête',b,'''Durée : 80 secondes.
MONTRER : parcourir les trois événements de gauche à droite, puis pointer la réponse négative du jeu.
DIRE : la première commande ne prend pas l’insecte. Le modèle va pourtant au sud et essaie ensuite de déposer un objet qu’il n’a pas. Il enchaîne des répétitions jusqu’à 30 coups, dont 29 non admissibles.
C’est une trace complète réelle et le premier échec simple par identifiant, pas un exemple inventé. L’insecte figure dans l’objectif : on ne peut pas appeler cela un objet halluciné. L’échec illustre un défaut de récupération après erreur. La faible couverture des états hors trajectoires expertes est une cause plausible du BC, sans être démontrée par ce seul cas.
L’invalidité est un proxy : des synonymes compris par le parseur peuvent être comptés non admissibles. Le diagnostic de boucle ignore le compteur de tours du feedback et recherche une répétition description/inventaire/commande.
TRANSITION : que peut-on conclure sans dépasser ce que les expériences montrent ?''')

    b=text(65,199,'LoRA mixte sur les jeux non vus',27,'#BCD0D8')
    b+=text(65,335,f"{count('lora_mixed','easy')}/40",112,'#A9BAFF',700)+text(445,335,f"{count('lora_mixed','advanced')}/40",112,'#FFB28D',700)
    b+=text(72,388,'jeux simples',28,BG)+text(452,388,'jeux avancés',28,BG)
    b+=line(65,435,1200,435,'#4E6472',2)
    b+=lines(65,493,['L’imitation fonctionne sur ce benchmark.','Les démonstrations mixtes améliorent notre agent.'],32,BG,47,600)
    b+=lines(65,602,['Une graine, objectifs explicites et davantage de données pour le mixte.',
                      'Suite : corriger les états où le modèle s’égare (DAgger).'],23,'#BCD0D8',34)
    add('Un petit modèle apprend, avec des limites',b,'''Durée : 65 secondes.
MONTRER : les deux grands nombres, puis revenir aux limites écrites en bas.
DIRE : le résultat positif est un adaptateur capable de gagner sur de nouveaux jeux générés. Le résultat négatif est le faible transfert du modèle simple et sa dépendance au contexte. Le modèle mixte reçoit davantage de données et d’updates : ne pas attribuer le gain uniquement à la complexité des démonstrations.
L’objectif public de TextWorld décrit souvent les étapes. Cela mesure largement le suivi de consignes, sans prouver une planification générale. Une seule graine de fine-tuning et des structures communes limitent les conclusions.
DAgger serait une suite : interroger l’expert dans les états visités par l’agent sur train, puis ajouter ces corrections. Nous ne l’avons pas implémenté.
CONCLURE : code, données, adaptateurs et traces sont archivés ; 18 tests Linux passent. Les paramètres, références et métriques sont en annexe pour les questions.''',True)

    write_deck(out,slides,'index.html','Présentation principale',assets)
    (out/'notes.md').write_text('# Notes de soutenance\n\n10 slides, environ 12 minutes. Les durées proposées totalisent environ 12 min 15 s.\nLes annexes servent aux questions.\n\n'+'\n\n'.join(f'## {i+1}. {title}\n\n{notes}' for i,(title,asset,notes) in enumerate(slides)))
    # Separate annex: avoids padding the main talk with implementation detail.
    slides=[];asset_prefix="annexe"
    b=lines(65,178,['Qwen2.5-0.5B-Instruct · LoRA q_proj/v_proj','r = 16 · α = 32 · dropout = 0,05','Learning rate = 2e−4 · batch 2 × accumulation 8','3 époques configurées · graine 42','Contexte 1024 tokens · greedy · 32 nouveaux tokens max'],28,INK,63)
    b+=text(65,565,'Simple : 355 exemples / 66 mises à jour. Mixte : 1179 / 219.',25,BLUE,600)
    b+=text(65,618,'Checkpoint : minimum de loss de validation. Pas de sélection sur test.',23)
    add('Annexe : réglages de l’expérience',b,'Versions et empreintes dans les training.json archivés. Temps de fine-tuning : 313,4 et 932,4 secondes. Les ensembles de validation diffèrent, donc ne pas comparer directement leurs losses.')
    b=text(65,165,'TEST FINAL · 40 JEUX PAR CONDITION',21,MUTED,700)
    headers=['Agent / niveau','Gagnés','Coups','Non admiss.','Revisites']
    xx=[65,575,730,885,1060]
    for x,h in zip(xx,headers):b+=text(x,216,h,22,INK,700)
    rows=[('Initial / simple','base','easy'),('LoRA simple / simple','lora_easy','easy'),('Sans historique / simple','lora_easy_h0','easy'),('LoRA mixte / simple','lora_mixed','easy'),('LoRA simple / avancé','lora_easy','advanced'),('LoRA mixte / avancé','lora_mixed','advanced')]
    for i,(label,a,l) in enumerate(rows):
        m=metrics[f'test/{a}_{l}'];yy=272+i*51
        if i%2==0:b+=rect(54,yy-31,1168,45,'#E9E9E1',0)
        for x,v in zip(xx,[label,f"{m['successes']}/40",f"{m['mean_steps_all']:.1f}",f"{100*m['invalid_action_rate']:.1f} %",f"{100*m['loop_episode_rate']:.1f} %"]):b+=text(x,yy,v,23)
    b+=lines(65,625,['Coups : tous épisodes. Non-admissibilité : proxy pondéré par le nombre de commandes.',
                       'Une revisite peut être utile. Table complète et IC dans results/rapport.md.'],19,MUTED,27)
    add('Annexe : au-delà du taux de réussite',b,'Les échecs longs pèsent fortement dans le taux de commandes non admissibles. La revisite est un diagnostic, pas une preuve de blocage. Les coups sur les seules réussites et les troncatures sont dans les logs.')
    b=lines(65,190,['Côté et al. — TextWorld (2018)','Hu et al. — LoRA (2021)','Ross et al. — DAgger (2011), extension envisagée','Qwen2.5-0.5B-Instruct — carte modèle officielle'],30,INK,67)
    b+=text(65,525,'github.com/Symbioose/rl-epita-s9',34,BLUE,700)
    b+=lines(65,588,['Références complètes : docs/REFERENCES.md','Traces, données et adaptateurs : archive de reproductibilité.'],24,MUTED,37)
    add('Annexe : sources et preuves',b,'https://arxiv.org/abs/1806.11532 ; https://arxiv.org/abs/2106.09685 ; https://arxiv.org/abs/1011.0686 ; https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct. Jericho et ALFWorld ne sont pas implémentés.')
    write_deck(out,slides,'annexes.html','Annexes',assets)
    print('10 slides visuelles + 3 annexes séparées générées.')


def write_deck(out,slides,filename,title,assets):
    sections=[]
    for i,(name,asset,notes) in enumerate(slides):
        encoded=base64.b64encode((assets/asset).read_bytes()).decode()
        sections.append(f'<section class="slide{" active" if i==0 else ""}" aria-label="{esc(name)}"><img src="data:image/svg+xml;base64,{encoded}" alt="{esc(name)}"><aside>{esc(notes).replace(chr(10),"<br>")}</aside></section>')
    css='''@page{size:1280px 720px;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#142939;font-family:Arial,sans-serif}body{overflow:hidden}#deck{position:absolute;width:1280px;height:720px;transform-origin:top left}.slide{position:relative;width:1280px;height:720px;display:none;overflow:hidden}.slide.active{display:block}.slide>img{display:block;width:1280px;height:720px}aside{display:none;position:absolute;left:40px;right:40px;bottom:35px;max-height:260px;overflow:auto;padding:24px;background:#fffdf7;border:2px solid #365cf5;color:#142939;font-size:22px;line-height:1.4}.notes aside{display:block}nav{position:fixed;right:18px;bottom:10px;display:flex;gap:8px;opacity:.25}nav:hover{opacity:1}button{border:0;border-radius:5px;padding:9px 12px;cursor:pointer}@media print{body{overflow:visible;background:white}#deck{position:static;height:auto;transform:none!important}.slide,.slide.active{display:block;break-after:page}aside,nav{display:none!important}}'''
    script='''let i=0;const slides=[...document.querySelectorAll('.slide')];function show(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,j)=>s.classList.toggle('active',j===i));location.hash=i+1}function move(d){show(i+d)}function notes(){document.body.classList.toggle('notes')}function full(){if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.()}function resize(){const d=document.getElementById('deck'),s=Math.min(innerWidth/1280,innerHeight/720);d.style.transform='scale('+s+')';d.style.left=(innerWidth-1280*s)/2+'px';d.style.top=(innerHeight-720*s)/2+'px'}addEventListener('resize',resize);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();move(1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='n')notes();if(e.key.toLowerCase()==='f')full()});resize();show((parseInt(location.hash.slice(1))||1)-1);'''
    html=f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="deck-layout" content="visual-v2"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{css}</style></head><body><main id="deck">'+''.join(sections)+'</main><nav><button onclick="move(-1)" aria-label="Précédente">←</button><button onclick="move(1)" aria-label="Suivante">→</button><button onclick="notes()">Notes (N)</button><button onclick="full()">Plein écran (F)</button></nav><script>'+script+'</script></body></html>'
    (out/filename).write_text(html)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',default='artifacts/eval/test');p.add_argument('--output',default=str(Path(__file__).parent));p.add_argument('--figure',help='Compatibilité avec l’ancien appel ; graphiques désormais recalculés depuis les mesures.')
    main(**vars(p.parse_args()))
