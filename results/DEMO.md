# Démonstration hors ligne

Ces extraits sont issus du test final. Aucun modèle ne tourne pour les relire.

## lora_easy — easy-30001 — victoire

Premier épisode correspondant, trié par identifiant.

Who's got a virtual machine and is about to play through an fast paced round of TextWorld? You do! Here is your task for today. First off, try to go to the east. Following that, open the type B locker within the kitchenette. And then, retrieve the fly larva from the type B locker in the kitchenette. That's it!

```text
01. go east | récompense=0.0 | score=0.0
02. open type B locker | récompense=0.0 | score=0.0
03. take fly larva from type B locker | récompense=1.0 | score=1.0
```

Bilan : 3 coups ; victoire=True ; non-admissibles=0.

Trace dans l’archive : `artifacts/eval/test/lora_easy_easy/traces/easy-30001.jsonl`.

## lora_easy — advanced-130000 — échec

Premier épisode correspondant, trié par identifiant.

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

```text
01. go east | récompense=0.0 | score=0.0
02. go west | récompense=0.0 | score=0.0
03. close hatch | récompense=0.0 | score=0.0
04. go south | récompense=0.0 | score=0.0
05. open hatch | récompense=0.0 | score=0.0
06. take keyboard | récompense=0.0 | score=0.0
07. close hatch | récompense=0.0 | score=0.0
08. go west | récompense=0.0 | score=0.0
09. open hatch | récompense=0.0 | score=0.0
10. take keyboard from floor | récompense=0.0 | score=0.0
```

Bilan : 30 coups ; victoire=False ; non-admissibles=15.
Les dix premiers coups sont montrés ; les autres sont conservés dans la trace complète.

Trace dans l’archive : `artifacts/eval/test/lora_easy_advanced/traces/advanced-130000.jsonl`.

## lora_mixed — advanced-130001 — victoire

Premier épisode correspondant, trié par identifiant.

Welcome to TextWorld! Here is your task for today. First thing I need you to do is to recover the passkey from the floor of the cookhouse. Then, make sure that the chest in the cookhouse is unlocked. Once you have unlocked the chest, open the chest within the cookhouse. Once you have pulled open the chest, pick up the keycard from the chest. After that, try to venture west. Following that, close the box. After that, assure that the box within the cubicle is locked. Got that? Good!

```text
01. take passkey | récompense=0.0 | score=0.0
02. unlock chest with passkey | récompense=0.0 | score=0.0
03. open chest | récompense=0.0 | score=0.0
04. take keycard from chest | récompense=1.0 | score=1.0
05. go west | récompense=0.0 | score=1.0
06. close box | récompense=0.0 | score=1.0
07. lock box with keycard | récompense=1.0 | score=2.0
```

Bilan : 7 coups ; victoire=True ; non-admissibles=0.

Trace dans l’archive : `artifacts/eval/test/lora_mixed_advanced/traces/advanced-130001.jsonl`.
