# management_game

Ce projet est un jeu de gestion basé sur les technologies natifs du web, HTML CSS et javascript, pour le backend nous utilisons python avec Flask et postgressql pour la base de données.

## 1. Configuration de la base de données:

- Dans le dossier [sql](https://github.com/LeSeulMano/management_game/tree/main/sql) vous trouverez deux fichiers, table.sql et start.sql. Le tables.sql s'occuper de créer toutes les tables nécéssaires au fonctionnement du jeu. Le fichier start.sql lui comporte toutes les commandes sql pour initialiser le projet. <br><br>

>__Malheureusement par manque de temps nous n'avons pas eu l'occasion de faire la gestion de village avec les utilisateurs. En théorie le fichier start.sql devrait ne pas exister__<br><br>

- Une fois les tables créés et le projet initialiser dans la base de données, rendez-vous dans le dossier site puis dans [lib](https://github.com/LeSeulMano/management_game/tree/main/site/lib). Dedans vous trouverez un fichier ```init_bdd.py``` ou vous pourrez renseigner les informations sur votre base de données (login, mot de passe ...) <br><br>

>__La configuration est terminé !__

## 2. Information:

 ### ⚠️ Les améliorations fonctionnent malheureusement par manque de temps un bug est présent lors que l'actualisation de la page lors qu'une amélioration est en cours
 <br>
 
 - L'ensemble du jeu a été réalisé, cependant certaines méthodes ne sont pas optimales comme le timer ou nous avons utilisé un setInterval, où encore pour les améliorations ou le timing se fait dans le javascript et non dans le backend (qui éviterait quelque bug). Pour remplacer le setInterval nous aurions pu passer par la lib ```Date```.<br>
   
 - La gestion des utilisateurs (la possibilité d'en avoir plusieurs, et que chaque utilisateur puisse avoir plusieurs villages) n'a pas été réaliser, cependant le terrain est préparé avec un peu plus de temps en plus cela aurait été possible sans grandes difficultées. <br>
 - En therme de faille détecté, la plus grande est l'id qui est affichée en haut de la page qui stocke en fait l'id de l'utilisateur connecté (laisser pour faire des tests), peut être changer par un attaquant. Nous récupérons le contenu de cette id dans le javascript pour ensuite l'envoyer au flask pour effectuer des requêtes, laissant donc __une vulnérabilité xss.__ <br>
 - Pour faciliter l'usage (et que nous n'avions pas le temps de gérer la vitesse du timer avec le x5 et x10) nous avons remplacé tous les timings en heure, par des timings en minutes.<br><br>


> Note: des fois le nombre de ressources s'affiche avec beaucoup de virgules malgré les arrondis, on ne sait pas pourquoi et par manque de temps ce bug ne reste pas corriger, il le sera surement pour la v2
