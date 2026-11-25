# Analyse de traces réelles

Sélection déterministe : trois échecs par condition au maximum, triés par identifiant de jeu.
Une action non admissible ne suffit pas à conclure à une hallucination.

## base_advanced — advanced-130000

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

Première commande non admissible au coup 1 : `west`.

Description visible :

-= Launderette =-
You've entered a launderette. The room seems oddly familiar, as though it were only superficially different from the other rooms in the building.

You make out a safe.

There is a closed hatch leading south. You need an unguarded exit? You should try going east.

Réponse du jeu :


You can't go that way.


>                                                                                                                                -= Launderette =-0/2

Séquence exécutée :

```text
01. west
02. south
03. west
04. south
05. west
06. south
07. west
08. south
09. west
10. south
11. west
12. south
13. west
14. south
15. west
16. south
17. west
18. south
19. west
20. south
21. west
22. south
23. west
24. south
25. west
26. south
27. west
28. south
29. west
30. south
```

## base_advanced — advanced-130001

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is your task for today. First thing I need you to do is to recover the passkey from the floor of the cookhouse. Then, make sure that the chest in the cookhouse is unlocked. Once you have unlocked the chest, open the chest within the cookhouse. Once you have pulled open the chest, pick up the keycard from the chest. After that, try to venture west. Following that, close the box. After that, assure that the box within the cubicle is locked. Got that? Good!

Première commande non admissible au coup 1 : `open chest`.

Description visible :

-= Cookhouse =-
You find yourself in a cookhouse. A typical one. Let's see what's in here.

You lean against the wall, inadvertently pressing a secret button. The wall opens up to reveal a chest, so there's that.

You need an unguarded exit? You should try going west.

There is a passkey on the floor.

Réponse du jeu :


You have to unlock the chest with the passkey first.


>                                                                                                                                -= Cookhouse =-0/2

Séquence exécutée :

```text
01. open chest
02. open chest
03. unlock chest
04. close box
05. open box
06. close box
07. open box
08. unlock chest
09. close box
10. open box
11. unlock chest
12. close box
13. open box
14. unlock chest
15. close box
16. open box
17. unlock chest
18. close box
19. open box
20. unlock chest
21. close box
22. open box
23. unlock chest
24. close box
25. open box
26. unlock chest
27. close box
28. open box
29. unlock chest
30. close box
```

## base_advanced — advanced-130002

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First step, recover the American limited edition passkey from the saucepan. Then, unlock the American limited edition box with the American limited edition passkey. Once you have unlocked the American limited edition box, make absolutely sure that the American limited edition box within the scullery is wide open. And then, make an effort to venture west. And then, recover the book from the box. And then, attempt to go to the east. Okay, and then, you can insert the book inside the American limited edition box inside the scullery. That's it!

Première commande non admissible au coup 1 : `open west`.

Description visible :

-= Scullery =-
You're now in a scullery.

You can make out a American limited edition box. Something scurries by right in the corner of your eye. Probably nothing. You make out a chest. As if things weren't amazing enough already, you can even see a saucepan. The saucepan is usual. On the saucepan you make out an American limited edition passkey.

There is an unguarded exit to the west.

Réponse du jeu :


You must name something more substantial.


>                                                                                                                                -= Scullery =-0/2

Séquence exécutée :

```text
01. open west
02. west
03. east
04. west
05. north
06. west
07. east
08. west
09. north-east
10. west-west
11. east-east
12. south-south
13. west-west
14. east-east
15. south-south
16. west-west
17. east-east
18. south-south
19. west-west
20. east-east
21. south-south
22. west-west
23. east-east
24. south-south
25. west-west
26. east-east
27. south-south
28. west-west
29. east-east
30. south-south
```

## base_easy — easy-30000

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Hey, thanks for coming over to the TextWorld today, there is something I need you to do for me. First of all, you could, like, retrieve the insect from the floor of the cookhouse. And then, make an attempt to go south. Then, put the insect on the mantle inside the chamber. That's it!

Première commande non admissible au coup 1 : `south`.

Description visible :

-= Cookhouse =-
You're now in a cookhouse.



You need an unblocked exit? You should try going south.

There is a carrot and an insect on the floor.

Réponse du jeu :



-= Chamber =-
Fancy seeing you here. Here, by the way, being the chamber. I guess you better just go and list everything you see here.

You can make out a basket. You can see a mantle. What a coincidence, weren't you just thinking about a mantle? The mantle is standard. But oh no! there's nothing on this piece of junk.

There is an unguarded exit to the north. There is an unguarded exit to the west.



>                                                                                                                                -= Chamber =-0/2

Séquence exécutée :

```text
01. south
02. west
03. east
04. south
05. west
06. north
07. east
08. south
09. west
10. east
11. north
12. south
13. west
14. east
15. north
16. south
17. west
18. east
19. north
20. south
21. west
22. east
23. north
24. south
25. west
26. east
27. north
28. south
29. west
30. east
```

## base_easy — easy-30001

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an fast paced round of TextWorld? You do! Here is your task for today. First off, try to go to the east. Following that, open the type B locker within the kitchenette. And then, retrieve the fly larva from the type B locker in the kitchenette. That's it!

Première commande non admissible au coup 1 : `south`.

Description visible :

-= Cubicle =-
You've entered a cubicle.



There is an exit to the east. Don't worry, it is unblocked. You need an unguarded exit? You should try going south.

Réponse du jeu :



-= Restroom =-
You're now in the restroom.

You can make out a locked TextWorld limited edition safe.

There is an unblocked exit to the north.



>                                                                                                                                -= Restroom =-0/2

Séquence exécutée :

```text
01. south
02. north
03. south
04. east
05. west
06. south
07. north
08. south
09. east
10. west
11. south
12. north
13. south
14. east
15. west
16. east
17. north
18. south
19. east
20. west
21. south
22. north
23. south
24. east
25. west
26. east
27. north
28. south
29. east
30. west
```

## base_easy — easy-30002

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is how to play! First off, if it's not too much trouble, I need you to venture south. Then, pick up the insect from the bench in the steam room. Then, ditch the insect on the floor of the steam room. Got that? Good!

Première commande non admissible au coup 1 : `south`.

Description visible :

-= Shower =-
You are in a shower. A normal kind of place. The room seems oddly familiar, as though it were only superficially different from the other rooms in the building.



You need an unblocked exit? You should try going south.

There is a loaf of bread on the floor.

Réponse du jeu :



-= Steam Room =-
You are in a steam room. A standard kind of place. You try to gain information on your surroundings by using a technique you call "looking."

You see a bench. The bench is standard. On the bench you can make out an insect. You can see a board. The board is usual. But there isn't a thing on it.

There is an unguarded exit to the north. You don't like doors? Why not try going west, that entranceway is unguarded.



>                                                                                                                                -= Steam Room =-0/2

Séquence exécutée :

```text
01. south
02. west
03. east
04. south
05. west
06. north
07. east
08. south
09. west
10. east
11. north
12. south
13. west
14. east
15. south
16. west
17. north
18. east
19. south
20. west
21. east
22. west
23. east
24. south
25. west
26. north
27. east
28. south
29. west
30. east
```

## lora_easy_advanced — advanced-130000

Coups : 30. Non admissibles : 15. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

Première commande non admissible au coup 3 : `close hatch`.

Description visible :

-= Launderette =-
You've entered a launderette. The room seems oddly familiar, as though it were only superficially different from the other rooms in the building.

You make out a safe.

There is a closed hatch leading south. You need an unguarded exit? You should try going east.

Réponse du jeu :


That's already closed.


>                                                                                                                                -= Launderette =-0/4

Séquence exécutée :

```text
01. go east
02. go west
03. close hatch
04. go south
05. open hatch
06. take keyboard
07. close hatch
08. go west
09. open hatch
10. take keyboard from floor
11. close hatch
12. go south
13. open hatch
14. take keyboard
15. close hatch
16. go west
17. open hatch
18. take keyboard from floor
19. close hatch
20. go west
21. open hatch
22. take keyboard from floor
23. close hatch
24. go west
25. open hatch
26. take keyboard from floor
27. close hatch
28. go west
29. open hatch
30. take keyboard from floor
```

## lora_easy_advanced — advanced-130001

Coups : 30. Non admissibles : 24. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is your task for today. First thing I need you to do is to recover the passkey from the floor of the cookhouse. Then, make sure that the chest in the cookhouse is unlocked. Once you have unlocked the chest, open the chest within the cookhouse. Once you have pulled open the chest, pick up the keycard from the chest. After that, try to venture west. Following that, close the box. After that, assure that the box within the cubicle is locked. Got that? Good!

Première commande non admissible au coup 1 : `take passkey from chest`.

Description visible :

-= Cookhouse =-
You find yourself in a cookhouse. A typical one. Let's see what's in here.

You lean against the wall, inadvertently pressing a secret button. The wall opens up to reveal a chest, so there's that.

You need an unguarded exit? You should try going west.

There is a passkey on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Cookhouse =-0/1

Séquence exécutée :

```text
01. take passkey from chest
02. take passkey from chest
03. unlock chest with passkey
04. open chest with passkey
05. close box
06. take keycard from chest
07. go west
08. open box
09. take keycard from chest
10. close box
11. open keycard
12. go west
13. unlock chest
14. close box
15. open chest
16. take keycard from chest
17. go west
18. unlock chest with keycard
19. close box
20. go west
21. open chest with keycard
22. go west
23. close box
24. go east
25. open box
26. take keycard from chest
27. close box
28. open chest
29. put keycard in box
30. unlock chest with keycard
```

## lora_easy_advanced — advanced-130002

Coups : 30. Non admissibles : 27. Revisite détectée : True. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First step, recover the American limited edition passkey from the saucepan. Then, unlock the American limited edition box with the American limited edition passkey. Once you have unlocked the American limited edition box, make absolutely sure that the American limited edition box within the scullery is wide open. And then, make an effort to venture west. And then, recover the book from the box. And then, attempt to go to the east. Okay, and then, you can insert the book inside the American limited edition box inside the scullery. That's it!

Première commande non admissible au coup 4 : `unlock American limited edition box with American limited edition passkey`.

Description visible :

-= Parlor =-
You've walked into a normal room. Your mind races to think of what kind of room would be normal. And then it hits you. Of course. You're in the parlor. You begin looking for stuff.

You can see an opened box. The box contains a book.

There is a closed door leading north. There is an exit to the east. Don't worry, it is unblocked.

Réponse du jeu :


I didn't understand that sentence.

>                                                                                                                                -= Parlor =-0/4

Séquence exécutée :

```text
01. take American limited edition passkey from saucepan
02. unlock American limited edition box with American limited edition passkey
03. go west
04. unlock American limited edition box with American limited edition passkey
05. go west
06. take American limited edition box from scullery
07. unlock American limited edition box with American limited edition passkey
08. go west
09. take American limited edition box from scullery
10. unlock American limited edition box with American limited edition passkey
11. go west
12. take American limited edition box from scullery
13. unlock American limited edition box with American limited edition passkey
14. go west
15. take American limited edition box from scullery
16. unlock American limited edition box with American limited edition passkey
17. go west
18. take American limited edition box from scullery
19. unlock American limited edition box with American limited edition passkey
20. go west
21. take American limited edition box from scullery
22. unlock American limited edition box with American limited edition passkey
23. go west
24. take American limited edition box from scullery
25. unlock American limited edition box with American limited edition passkey
26. go west
27. take American limited edition box from scullery
28. unlock American limited edition box with American limited edition passkey
29. go west
30. take American limited edition box from scullery
```

## lora_easy_easy — easy-30000

Coups : 30. Non admissibles : 29. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Hey, thanks for coming over to the TextWorld today, there is something I need you to do for me. First of all, you could, like, retrieve the insect from the floor of the cookhouse. And then, make an attempt to go south. Then, put the insect on the mantle inside the chamber. That's it!

Première commande non admissible au coup 1 : `take insect from floor`.

Description visible :

-= Cookhouse =-
You're now in a cookhouse.



You need an unblocked exit? You should try going south.

There is a carrot and an insect on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Cookhouse =-0/1

Séquence exécutée :

```text
01. take insect from floor
02. go south
03. put insect on mantle
04. take insect from mantle
05. go south
06. insert insect into mantle
07. put insect on mantle
08. take insect from mantle
09. go south
10. insert insect into mantle
11. put insect on mantle
12. take insect from mantle
13. go south
14. insert insect into mantle
15. put insect on mantle
16. take insect from mantle
17. go south
18. insert insect into mantle
19. put insect on mantle
20. take insect from mantle
21. go south
22. insert insect into mantle
23. put insect on mantle
24. take insect from mantle
25. go south
26. insert insect into mantle
27. put insect on mantle
28. take insect from mantle
29. go south
30. insert insect into mantle
```

## lora_easy_easy — easy-30003

Coups : 30. Non admissibles : 29. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an fast paced round of TextWorld? You do! Here is how to play! First, it would be good if you could try to take a trip south. And then, head east. Then, ensure that the rectangular box is open. That's it!

Première commande non admissible au coup 2 : `open rectangular box`.

Description visible :

-= Restroom =-
You've just sauntered into a restroom.



You need an unguarded exit? You should try going east. There is an unblocked exit to the north.

There is a pear on the floor.

Réponse du jeu :


I only understood you as far as wanting to open the rectangular passkey.

>                                                                                                                                -= Restroom =-0/2

Séquence exécutée :

```text
01. go south
02. open rectangular box
03. close rectangular box
04. open rectangular box
05. exit
06. put rectangular passkey in rectangular box
07. unlock rectangular box with rectangular passkey
08. close rectangular box
09. insert rectangular passkey into rectangular box
10. open rectangular box with rectangular passkey
11. exit rectangular box
12. insert rectangular passkey into rectangular box
13. close rectangular box with rectangular passkey
14. take rectangular passkey from rectangular box
15. open rectangular box with rectangular passkey
16. exit restroom
17. insert rectangular passkey into rectangular box
18. close rectangular box with rectangular passkey
19. put rectangular passkey in rectangular box with feedback
20. open rectangular box with feedback
21. take rectangular passkey from rectangular box with feedback
22. close rectangular box with feedback
23. insert rectangular passkey into rectangular box with feedback
24. close rectangular box with feedback
25. open rectangular box with feedback
26. insert rectangular passkey into rectangular box with feedback
27. take rectangular passkey from rectangular box with feedback
28. unlock rectangular box with feedback
29. close rectangular box with feedback
30. insert rectangular passkey into rectangular box with feedback
```

## lora_easy_easy — easy-30006

Coups : 30. Non admissibles : 29. Revisite détectée : True. Limite atteinte : True.

Objectif public :

It's time to explore the amazing world of TextWorld! Here is how to play! Your first objective is to travel north. Then, take a trip east. Then, make sure that the fudge scented locker within the vault is closed. And once you've done that, you win!

Première commande non admissible au coup 2 : `close fudge scented locker`.

Description visible :

-= Cookery =-
You are in a cookery. A standard kind of place.



There is an exit to the east. Don't worry, it is unblocked. There is an exit to the south. Don't worry, it is unguarded.

There is a spork on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Cookery =-0/2

Séquence exécutée :

```text
01. go north
02. close fudge scented locker
03. lock fudge scented locker with key
04. close fudge scented locker
05. unlock fudge scented locker with key
06. close fudge scented locker
07. lock fudge scented locker with key
08. success
09. undo lock fudge scented locker with key
10. unlock fudge scented locker with key
11. close fudge scented locker
12. success
13. lock fudge scented locker with key
14. close fudge scented locker
15. success
16. unlock fudge scented locker with key
17. close fudge scented locker
18. success
19. lock fudge scented locker with key
20. close fudge scented locker
21. success
22. unlock fudge scented locker with key
23. close fudge scented locker
24. success
25. lock fudge scented locker with key
26. close fudge scented locker
27. success
28. unlock fudge scented locker with key
29. close fudge scented locker
30. success
```

## lora_easy_h0_advanced — advanced-130000

Coups : 30. Non admissibles : 8. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

Première commande non admissible au coup 4 : `go west`.

Description visible :

-= Launderette =-
You've entered a launderette. The room seems oddly familiar, as though it were only superficially different from the other rooms in the building.

You make out a safe.

There is an open hatch leading south. You need an unguarded exit? You should try going east.

Réponse du jeu :


You can't go that way.


>                                                                                                                                -= Launderette =-0/5

Séquence exécutée :

```text
01. go east
02. go west
03. open hatch
04. go west
05. go west
06. go west
07. go west
08. go west
09. go east
10. go west
11. go east
12. go west
13. go east
14. go west
15. go east
16. go west
17. go east
18. take keyboard from floor
19. go west
20. go east
21. go west
22. go east
23. take keyboard from floor
24. go west
25. go east
26. go west
27. go east
28. go west
29. go east
30. take keyboard from floor
```

## lora_easy_h0_advanced — advanced-130001

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is your task for today. First thing I need you to do is to recover the passkey from the floor of the cookhouse. Then, make sure that the chest in the cookhouse is unlocked. Once you have unlocked the chest, open the chest within the cookhouse. Once you have pulled open the chest, pick up the keycard from the chest. After that, try to venture west. Following that, close the box. After that, assure that the box within the cubicle is locked. Got that? Good!

Première commande non admissible au coup 1 : `take passkey from chest`.

Description visible :

-= Cookhouse =-
You find yourself in a cookhouse. A typical one. Let's see what's in here.

You lean against the wall, inadvertently pressing a secret button. The wall opens up to reveal a chest, so there's that.

You need an unguarded exit? You should try going west.

There is a passkey on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Cookhouse =-0/1

Séquence exécutée :

```text
01. take passkey from chest
02. take passkey from chest
03. take passkey from chest
04. take passkey from chest
05. take passkey from chest
06. take passkey from chest
07. take passkey from chest
08. take passkey from chest
09. take passkey from chest
10. take passkey from chest
11. take passkey from chest
12. take passkey from chest
13. take passkey from chest
14. take passkey from chest
15. take passkey from chest
16. take passkey from chest
17. take passkey from chest
18. take passkey from chest
19. take passkey from chest
20. take passkey from chest
21. take passkey from chest
22. take passkey from chest
23. take passkey from chest
24. take passkey from chest
25. take passkey from chest
26. take passkey from chest
27. take passkey from chest
28. take passkey from chest
29. take passkey from chest
30. take passkey from chest
```

## lora_easy_h0_advanced — advanced-130002

Coups : 30. Non admissibles : 28. Revisite détectée : True. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First step, recover the American limited edition passkey from the saucepan. Then, unlock the American limited edition box with the American limited edition passkey. Once you have unlocked the American limited edition box, make absolutely sure that the American limited edition box within the scullery is wide open. And then, make an effort to venture west. And then, recover the book from the box. And then, attempt to go to the east. Okay, and then, you can insert the book inside the American limited edition box inside the scullery. That's it!

Première commande non admissible au coup 3 : `take American limited edition box`.

Description visible :

-= Scullery =-
You're now in a scullery.

You can make out a American limited edition box. Something scurries by right in the corner of your eye. Probably nothing. You make out a chest. As if things weren't amazing enough already, you can even see a saucepan. The saucepan is usual. But there isn't a thing on it.

There is an unguarded exit to the west.

Réponse du jeu :


That's fixed in place.



>                                                                                                                                -= Scullery =-0/4

Séquence exécutée :

```text
01. take American limited edition passkey from saucepan
02. unlock American limited edition box with American limited edition passkey
03. take American limited edition box
04. unlock American limited edition box with American limited edition passkey
05. take American limited edition box from saucepan
06. take American limited edition passkey from saucepan
07. take American limited edition passkey from saucepan
08. take American limited edition passkey from saucepan
09. take American limited edition passkey from saucepan
10. take American limited edition passkey from saucepan
11. take American limited edition passkey from saucepan
12. take American limited edition passkey from saucepan
13. take American limited edition passkey from saucepan
14. take American limited edition passkey from saucepan
15. take American limited edition passkey from saucepan
16. take American limited edition passkey from saucepan
17. take American limited edition passkey from saucepan
18. take American limited edition passkey from saucepan
19. take American limited edition passkey from saucepan
20. take American limited edition passkey from saucepan
21. take American limited edition passkey from saucepan
22. take American limited edition passkey from saucepan
23. take American limited edition passkey from saucepan
24. take American limited edition passkey from saucepan
25. take American limited edition passkey from saucepan
26. take American limited edition passkey from saucepan
27. take American limited edition passkey from saucepan
28. take American limited edition passkey from saucepan
29. take American limited edition passkey from saucepan
30. take American limited edition passkey from saucepan
```

## lora_easy_h0_easy — easy-30000

Coups : 30. Non admissibles : 30. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Hey, thanks for coming over to the TextWorld today, there is something I need you to do for me. First of all, you could, like, retrieve the insect from the floor of the cookhouse. And then, make an attempt to go south. Then, put the insect on the mantle inside the chamber. That's it!

Première commande non admissible au coup 1 : `take insect from floor`.

Description visible :

-= Cookhouse =-
You're now in a cookhouse.



You need an unblocked exit? You should try going south.

There is a carrot and an insect on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Cookhouse =-0/1

Séquence exécutée :

```text
01. take insect from floor
02. take insect from floor
03. take insect from floor
04. take insect from floor
05. take insect from floor
06. take insect from floor
07. take insect from floor
08. take insect from floor
09. take insect from floor
10. take insect from floor
11. take insect from floor
12. take insect from floor
13. take insect from floor
14. take insect from floor
15. take insect from floor
16. take insect from floor
17. take insect from floor
18. take insect from floor
19. take insect from floor
20. take insect from floor
21. take insect from floor
22. take insect from floor
23. take insect from floor
24. take insect from floor
25. take insect from floor
26. take insect from floor
27. take insect from floor
28. take insect from floor
29. take insect from floor
30. take insect from floor
```

## lora_easy_h0_easy — easy-30001

Coups : 30. Non admissibles : 29. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an fast paced round of TextWorld? You do! Here is your task for today. First off, try to go to the east. Following that, open the type B locker within the kitchenette. And then, retrieve the fly larva from the type B locker in the kitchenette. That's it!

Première commande non admissible au coup 2 : `go east`.

Description visible :

-= Kitchenette =-
You are in a kitchenette. It seems to be pretty standard here.

You see a closed type B locker in the room.

There is an unguarded exit to the west.

There is a type B passkey on the floor.

Réponse du jeu :


You can't go that way.


>                                                                                                                                -= Kitchenette =-0/3

Séquence exécutée :

```text
01. go east
02. go east
03. go east
04. go east
05. go east
06. go east
07. go east
08. go east
09. go east
10. go east
11. go east
12. go east
13. go east
14. go east
15. go east
16. go east
17. go east
18. go east
19. go east
20. go east
21. go east
22. go east
23. go east
24. go east
25. go east
26. go east
27. go east
28. go east
29. go east
30. go east
```

## lora_easy_h0_easy — easy-30002

Coups : 30. Non admissibles : 28. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is how to play! First off, if it's not too much trouble, I need you to venture south. Then, pick up the insect from the bench in the steam room. Then, ditch the insect on the floor of the steam room. Got that? Good!

Première commande non admissible au coup 2 : `go south`.

Description visible :

-= Steam Room =-
You are in a steam room. A standard kind of place. You try to gain information on your surroundings by using a technique you call "looking."

You see a bench. The bench is standard. On the bench you can make out an insect. You can see a board. The board is usual. But there isn't a thing on it.

There is an unguarded exit to the north. You don't like doors? Why not try going west, that entranceway is unguarded.

Réponse du jeu :


You can't go that way.


>                                                                                                                                -= Steam Room =-0/3

Séquence exécutée :

```text
01. go south
02. go south
03. take insect from bench
04. go south
05. go south
06. go south
07. go south
08. go south
09. go south
10. go south
11. go south
12. go south
13. go south
14. go south
15. go south
16. go south
17. go south
18. go south
19. go south
20. go south
21. go south
22. go south
23. go south
24. go south
25. go south
26. go south
27. go south
28. go south
29. go south
30. go south
```

## lora_mixed_advanced — advanced-130000

Coups : 30. Non admissibles : 23. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

Première commande non admissible au coup 7 : `take keyboard from floor`.

Description visible :

-= Spare Room =-
You find yourself in a spare room. A standard kind of place.

What's that over there? It looks like it's a stand. The stand is standard. On the stand you make out a shirt. Oh wow! Is that what I think it is? It is! It's a workbench. But the thing is empty, unfortunately. It would have been so cool if there was stuff on the workbench.

There is an exit to the north. Don't worry, it is unguarded. There is an unblocked exit to the west.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Spare Room =-1/7

Séquence exécutée :

```text
01. go east
02. take keyboard
03. go west
04. open hatch
05. go south
06. go south
07. take keyboard from floor
08. go west
09. open hatch
10. go south
11. go west
12. open hatch
13. go south
14. go south
15. go south
16. go south
17. go south
18. go south
19. go south
20. go south
21. go south
22. go south
23. go south
24. go south
25. go south
26. go south
27. go south
28. go south
29. go south
30. go south
```

## lora_mixed_advanced — advanced-130002

Coups : 30. Non admissibles : 18. Revisite détectée : True. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First step, recover the American limited edition passkey from the saucepan. Then, unlock the American limited edition box with the American limited edition passkey. Once you have unlocked the American limited edition box, make absolutely sure that the American limited edition box within the scullery is wide open. And then, make an effort to venture west. And then, recover the book from the box. And then, attempt to go to the east. Okay, and then, you can insert the book inside the American limited edition box inside the scullery. That's it!

Première commande non admissible au coup 5 : `open box`.

Description visible :

-= Parlor =-
You've walked into a normal room. Your mind races to think of what kind of room would be normal. And then it hits you. Of course. You're in the parlor. You begin looking for stuff.

You can see an opened box. The box contains a book.

There is a closed door leading north. There is an exit to the east. Don't worry, it is unblocked.

Réponse du jeu :


That's already open.


>                                                                                                                                -= Parlor =-1/6

Séquence exécutée :

```text
01. take American limited edition passkey from saucepan
02. unlock American limited edition box with American limited edition passkey
03. open American limited edition box
04. go west
05. open box
06. unlock box with American limited edition passkey
07. go west
08. go east
09. open American limited edition box
10. unlock American limited edition box with American limited edition passkey
11. open American limited edition box
12. go west
13. open box
14. go east
15. open American limited edition box
16. unlock American limited edition box with American limited edition passkey
17. open American limited edition box
18. go west
19. open box
20. go east
21. open American limited edition box
22. unlock American limited edition box with American limited edition passkey
23. open American limited edition box
24. go west
25. open box
26. go east
27. open American limited edition box
28. unlock American limited edition box with American limited edition passkey
29. open American limited edition box
30. go west
```

## lora_mixed_advanced — advanced-130005

Coups : 30. Non admissibles : 27. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Get ready to pick stuff up and put it in places, because you've just entered TextWorld! Here is your task for today. Your first objective is to doublecheck that the rectangular box is unlocked. If you have unlocked the rectangular box, open the rectangular box in the shower. And then, recover the sponge from the rectangular box in the shower. Then, pick up the latchkey from the floor of the shower. After that, make absolutely sure that the safe in the shower is unlocked. And then, ensure that the safe inside the shower is open. After that, put the sponge inside the safe within the shower. Once that's all handled, you can stop!

Première commande non admissible au coup 4 : `go to safe`.

Description visible :

-= Shower =-
You arrive in a shower. An ordinary one.

You can see a locked safe. You can see a rectangular box. The rectangular box is empty! This is the worst thing that could possibly happen, ever! You see a table. But the thing is empty.

There is a closed portal leading east. There is a closed hatch leading west.

There is a latchkey on the floor.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Shower =-1/4

Séquence exécutée :

```text
01. unlock rectangular box with rectangular keycard
02. open rectangular box
03. take sponge from rectangular box
04. go to safe
05. unlock safe with latchkey
06. take latchkey from floor
07. unlock safe with latchkey
08. unlock safe with latchkey
09. open safe
10. unlock safe with latchkey
11. take latchkey from floor
12. unlock safe with latchkey
13. unlock safe with latchkey
14. open safe
15. unlock safe with latchkey
16. take latchkey from floor
17. unlock safe with latchkey
18. unlock safe with latchkey
19. open safe
20. unlock safe with latchkey
21. take latchkey from floor
22. insert latchkey into rectangular box
23. unlock safe with latchkey
24. unlock safe with latchkey
25. unlock safe with latchkey
26. unlock safe with latchkey
27. unlock safe with latchkey
28. unlock safe with latchkey
29. unlock safe with latchkey
30. unlock safe with latchkey
```

## lora_mixed_easy — easy-30012

Coups : 30. Non admissibles : 20. Revisite détectée : True. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First off, make an effort to move east. With that done, pick up the bowl from the floor of the scullery. After you have taken the bowl, you can deposit the bowl into the fridge in the scullery. That's it!

Première commande non admissible au coup 6 : `eat chocolate bar`.

Description visible :

-= Parlor =-
You've just sauntered into a parlor.



There is an exit to the south. Don't worry, it is unguarded.

Réponse du jeu :


You can't see any such thing.

>                                                                                                                                -= Parlor =-0/6

Séquence exécutée :

```text
01. go east
02. take bowl
03. drop bowl
04. go west
05. go north
06. eat chocolate bar
07. take chocolate bar from fridge
08. insert chocolate bar into fridge
09. drop chocolate bar
10. go south
11. go north
12. eat bowl
13. insert bowl into fridge
14. drop bowl
15. go fridge
16. put bowl in fridge
17. insert bowl
18. take bowl
19. drop bowl
20. go south
21. go north
22. insert bowl into fridge
23. take bowl from floor
24. drop bowl
25. go fridge
26. put bowl in fridge
27. insert bowl into fridge
28. take bowl from scullery
29. drop bowl
30. go south
```

## random_advanced — advanced-130000

Coups : 30. Non admissibles : 0. Revisite détectée : False. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an life changing round of TextWorld? You do! First of all, attempt to travel east. Next, recover the keyboard from the floor of the study. After getting the keyboard, venture west. With that accomplished, ensure that the hatch inside the launderette is open. And then, make an effort to go south. If you can succeed at that, go to the south. With that over with, place the keyboard on the stand inside the spare room. And if you do that, you're the winner!

Séquence exécutée :

```text
01. open safe
02. close safe
03. examine fly larva
04. examine safe
05. look
06. drop licorice strip
07. examine licorice strip
08. drop fly larva
09. inventory
10. examine safe
11. open hatch
12. inventory
13. take fly larva
14. take licorice strip
15. open safe
16. go east
17. take keyboard
18. eat licorice strip
19. inventory
20. examine keyboard
21. go west
22. inventory
23. insert keyboard into safe
24. close safe
25. open safe
26. close hatch
27. drop fly larva
28. examine safe
29. inventory
30. open hatch
```

## random_advanced — advanced-130001

Coups : 30. Non admissibles : 0. Revisite détectée : False. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is your task for today. First thing I need you to do is to recover the passkey from the floor of the cookhouse. Then, make sure that the chest in the cookhouse is unlocked. Once you have unlocked the chest, open the chest within the cookhouse. Once you have pulled open the chest, pick up the keycard from the chest. After that, try to venture west. Following that, close the box. After that, assure that the box within the cubicle is locked. Got that? Good!

Séquence exécutée :

```text
01. drop towel
02. examine spoon
03. look
04. take passkey
05. examine chest
06. inventory
07. go west
08. examine passkey
09. take Quote of the Day Calendar
10. drop Quote of the Day Calendar
11. insert passkey into box
12. examine spoon
13. insert spoon into box
14. take passkey from box
15. insert licorice strip into box
16. drop passkey
17. take spoon from box
18. close box
19. take passkey
20. drop spoon
21. examine spoon
22. take Quote of the Day Calendar
23. drop passkey
24. look
25. inventory
26. open box
27. examine licorice strip
28. examine Quote of the Day Calendar
29. examine gateway
30. inventory
```

## random_advanced — advanced-130002

Coups : 30. Non admissibles : 0. Revisite détectée : False. Limite atteinte : True.

Objectif public :

I hope you're ready to go into rooms and interact with objects, because you've just entered TextWorld! Here is your task for today. First step, recover the American limited edition passkey from the saucepan. Then, unlock the American limited edition box with the American limited edition passkey. Once you have unlocked the American limited edition box, make absolutely sure that the American limited edition box within the scullery is wide open. And then, make an effort to venture west. And then, recover the book from the box. And then, attempt to go to the east. Okay, and then, you can insert the book inside the American limited edition box inside the scullery. That's it!

Séquence exécutée :

```text
01. examine disk
02. put disk on saucepan
03. drop loaf of bread
04. open chest
05. inventory
06. insert teapot into chest
07. take American limited edition passkey from saucepan
08. examine disk
09. examine chest
10. examine teapot
11. examine saucepan
12. examine American limited edition box
13. look
14. take loaf of bread
15. examine disk
16. examine passkey
17. unlock American limited edition box with American limited edition passkey
18. examine teapot
19. go west
20. drop American limited edition passkey
21. drop loaf of bread
22. examine door
23. take American limited edition passkey
24. take loaf of bread
25. insert American limited edition passkey into box
26. take book from box
27. insert book into box
28. examine passkey
29. examine loaf of bread
30. examine book
```

## random_easy — easy-30000

Coups : 30. Non admissibles : 0. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Hey, thanks for coming over to the TextWorld today, there is something I need you to do for me. First of all, you could, like, retrieve the insect from the floor of the cookhouse. And then, make an attempt to go south. Then, put the insect on the mantle inside the chamber. That's it!

Séquence exécutée :

```text
01. eat loaf of bread
02. take insect
03. inventory
04. examine carrot
05. examine insect
06. inventory
07. look
08. look
09. look
10. inventory
11. drop insect
12. go south
13. examine basket
14. open basket
15. examine basket
16. go north
17. examine carrot
18. go south
19. examine basket
20. examine basket
21. close basket
22. open basket
23. go north
24. take insect
25. take carrot
26. examine insect
27. look
28. examine carrot
29. look
30. go south
```

## random_easy — easy-30001

Coups : 30. Non admissibles : 0. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Who's got a virtual machine and is about to play through an fast paced round of TextWorld? You do! Here is your task for today. First off, try to go to the east. Following that, open the type B locker within the kitchenette. And then, retrieve the fly larva from the type B locker in the kitchenette. That's it!

Séquence exécutée :

```text
01. inventory
02. look
03. go south
04. unlock TextWorld limited edition safe with TextWorld limited edition latchkey
05. examine TextWorld limited edition latchkey
06. examine TextWorld limited edition latchkey
07. go north
08. drop TextWorld limited edition latchkey
09. inventory
10. inventory
11. go east
12. examine type B locker
13. take type B passkey
14. drop type B passkey
15. inventory
16. take type B passkey
17. examine type B passkey
18. examine type B passkey
19. lock type B locker with type B passkey
20. go west
21. examine TextWorld limited edition latchkey
22. look
23. go south
24. go north
25. go east
26. examine type B locker
27. inventory
28. unlock type B locker with type B passkey
29. lock type B locker with type B passkey
30. unlock type B locker with type B passkey
```

## random_easy — easy-30002

Coups : 30. Non admissibles : 0. Revisite détectée : True. Limite atteinte : True.

Objectif public :

Welcome to TextWorld! Here is how to play! First off, if it's not too much trouble, I need you to venture south. Then, pick up the insect from the bench in the steam room. Then, ditch the insect on the floor of the steam room. Got that? Good!

Séquence exécutée :

```text
01. go south
02. examine board
03. go west
04. examine book
05. inventory
06. examine book
07. inventory
08. take book
09. look
10. inventory
11. examine book
12. look
13. go east
14. put book on bench
15. examine board
16. take insect from bench
17. go west
18. inventory
19. drop insect
20. examine insect
21. inventory
22. look
23. go east
24. go north
25. go south
26. examine book
27. go west
28. go east
29. examine board
30. take book from bench
```
