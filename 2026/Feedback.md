# General
- Etre 3 enseignants serait plus confortable
- Modifier slides pour ne plus faire référence à chabotv
- Demander à la gestionnaire des emplois du temps, Maguy Bousserie, de ne pas avoir la petite salle C057
- Demander à rencontrer le responsable d'UE (au moins) pour avoir une coordination des cours entre enseignants.
- Demander à avoir le retour des élèves en fin d'année

# 01 - Unix CLI

- Je trouverais plus naturel d'introduire `pwd` et `~` avant `ls`.

# 02 - Venv (30' max)
- Pour éviter les confusions, donner un autre nom à l'alias : alias go_totoro="..."

# 03 - Python et Numpy

- On pourrait rallonger cette partie si besoin

# 04 - La Station (pandas)

- [x] Expliquer ce qu'est un "dataframe"
- Donner le lien vers la doc pandas?
- Renommer `read_station_data()` en `select_station_data()` or `extract_...`
- Nuancer le problème de lire plusieurs stations : pandas est intelligent et ne relis pas 1000 fois le même fichier (un mécanisme de mémoire cache peut-être)
- Rappeler dans les dates qu'il n'y a que 2018
- Les réponses sur la fin ne répondent pas vraiment aux questions. Les questions pourraient être réordonnées d'ailleurs.
- La réponse est dans le pdf "student" pour le premier exercice, à enlever
- "t", "hu", "max", "min" entre double quotes
- Rename "aggregation()" -> "aggregate()"
- Incertitude sur la période à regarder : dire à la première apparition de la période : dans cet exercice *et les suivants*. Ou préciser "période de votre choix" dans les derniers exos
- Question sur le premier max pas clair : dire "date/heure où la température maximale de la période est atteinte pour la première fois"

# 05 - Object-oriented programmation
- Have a python script ready to be used as a starter (what is already on slides, in py format)
- Exercice Reseau : indiquer qu'on peut s'inspirer de l'exemple plus loin pour savoir quelles fonctionnalités le réseau doit implémenter. Correction : remplacer id par station_id
- Général : trop abrupt, pas assez progressif et pas assez de contenu théorique. La difficulté de la gestion des csv/dataframes se rajoute à la difficulté de la découverte des objets. Rajouter une planche intermédiaire ou deux, avec une classe sans méthodes, une classe avec juste un constructeur...  Sinon, les orienter vers un cours en ligne, type openclassroom ou courspython.com.
- Mettre en gras les mots à retenir : classe, instance, attribut de données, méthode, constructeur
- Commenter la majuscule en première lettre des noms de classe, sur la portée des définitions (scope), sur la notion d'attribut 'privé' ou 'protégé'.
- Montrer en fin de cours ce que donne `dir(ma_station)`. Leur montrer qu'un dataframe est aussi un objet.
