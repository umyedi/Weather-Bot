# Weather Bot

---


## Introduction
Bonjour ! </br>
Nous sommes une **équipe de trois lycéens** ayant un **projet d'école** à sujet libre. Nous avons donc choisi de créer un **bot twitter** qui **publie la météo** d'une ville spécifique. Le bot peut également **changer sa photo de profil selon la météo**.

⚠️ Le fichier [application.py](https://github.com/Timoleroux/Weather-Bot/blob/main/application.py) est en cours de développement donc il est très probable que le code ne soit pas optimisé et qu'il y ait quelques bugs.

## C'est quoi le but ?

Weather Bot est un **bot codé entièrement en python** qui permet de **poster des tweets** annonçant la **météo** de n'importe quelle ville. On peut également programmer un **emploi du temps** où chaque jour, un tweet se postera aux heures prédéfinies.

---

## Prérequis pour lancer le script

**Attention :** *il est recommandé d'exécuter le script avec la **version 3.10** de [**Python**](https://www.python.org/downloads/) minimum.*
Pour télécharger le .zip, cliquez [ici](https://github.com/Timoleroux/Weather-Bot/archive/refs/heads/main.zip)

Pour traiter les données de Twitter, c'est le module [**Tweepy**](https://www.tweepy.org/) qui s'en charge. Pour y avoir accès, il faut installer le module en exécutant la commande :
    
    pip install tweepy

Il est également nécessaire de posséder les tokens de Tweepy. Pour cela, il faut se rendre sur l'[espace développeur](https://developer.twitter.com/en/portal/petition/essential/basic-info) de twitter et créer un projet pour récupérer les tokens nécessaires et les ajouter dans le fichier [ressources.py](https://github.com/Timoleroux/Weather-Bot/blob/main/ressources.py).

Pour traiter les données météorologiques, c'est le module [**Pyowm**](https://pypi.org/project/pyowm/) qui s'en charge. Pour y avoir accès, il faut installer le module en exécutant la commande :

    pip install pyowm

Il est aussi nécessaire de posséder le token de Pyowm. Pour cela, il faut se créer un compte sur [OWM](https://home.openweathermap.org/users/sign_up) puis, une fois connecté, se rendre [ici](https://home.openweathermap.org/api_keys) où vous trouverez le token nécessaire que vous pourrez ajouter au fichier [ressources.py](https://github.com/Timoleroux/Weather-Bot/blob/main/ressources.py).

**Attention :** nous ne connaissons pas l'emplacement des stations météo grâce auxquelles cette API va chercher les informations. Par conséquent, il est probable qu'il y ait des légères différences avec les données fournies par des sites de météo officiels.

Si les différences de données sont trop importantes, il est possible que la ville que vous avez entrée ait été confondue avec un autre endroit portant le même nom *(Ex : la ville de Brest existe en France et en Biélorussie)*.

---
## Documentation des fonctions

### ressources.py/AuthTweepy

    AuthTweepy()

Cette fonction permet d'**authentifier la connexion à Tweepy** et donc d'utiliser cette API. Voir la [doc officielle](https://docs.tweepy.org/en/stable/).

### ressources.py/AuthPyowm

    AuthPyowm()

Cette fonction permet d'**authentifier la connexion à Pyowm** et donc d'utiliser cette API. Voir la [doc officielle](https://pyowm.readthedocs.io/en/latest/).

### ressources.py/currentTime

    currentTime()
    Input : '%d/%m/%Y %H:%M:%S'
    Output : 05/11/2022 19:00:00

Cette fonction prend en entrée une chaine de caractères qui définit le format de l'heure qui sera retournée en sortie de la forme choisie.

| Commande |  Français  |  Anglais  |
|:--------:|:----------:|:---------:|
|   `%Y`   |   Année    |   Year    |
|   `%m`   |    Mois    |   Month   |
|   `%d`   |    Jour    |    Day    |
|   `%H`   |   Heure    |   Hour    |
|   `%M`   |   Minute   |  Minute   |
|   `%S`   |  Seconde   |  Second   |

### main.py/allWeatherInfos

    allWeatherInfos()
    Input : 'Paris'
    Output : ['Paris', '05/11/2022', '19h00', 'nuageux', 10, 9, 16.67]

Cette fonction prend en entrée un **nom de ville** sous forme de **string**.
Grâce à Pyowm, elle retourne une liste contenant les informations suivantes (ou `False` si la ville n'est pas valide) :
1. La **ville** qui a été entrée *(string)*
2. La **date du jour** sous la forme : JJ/MM/AAAA *(string)*
3. L'**heure du jour** sous la forme : 23h59 *(string)*
4. La **météo** *(string)*
5. La **température** de la ville *(int)*
6. Le **ressenti** de cette température *(int)*
7. La **vitesse du vent** dans cette ville *(float)*

### main.py/updateProfilPicture

    updateProfilPicture()
    Input : 'nuageux'
    Output : True

Cette fonction prend en entrée le 4<sup>ème</sup> élément de la liste précédente (la météo). </br>
Si l'entrée fait partie des cas cités dans la fonction, alors elle change la photo de profil du bot et retourne `True`. </br>
Si l'entrée ne fait pas partie des cas cités dans la fonction, alors elle affiche dans la console « Aucune photo de profil correspond à {météo} pour le moment. » et retourne `False`.

### main.py/publishTweet

    publishTweet()
    Input : ['Paris', '05/11/2022', '19h00', 'nuageux', 10, 9, 16.67]
    Output : Voici la météo pour Paris, le 05/11/2022 à 19h00:
                ☀️ Temps : nuageux
                🌡️ Température moyenne : 10°C (ressenti 9°C)
                💨 Vitesse du vent : 16.67 km/h

Cette fonction prend en entrée la liste de données que retourne la fonction [`allWeatherInfos()`](#mainpyallweatherinfos). </br>
Elle publie un tweet grâce à la liste qui lui a été donnée. Si l'opération réussit, elle retourne le tweet sinon elle retourne `False`.

### main.py/manualRun

    manualRun()
    Input : None
    Output : True

Cette fonction prend entrée une ville sous forme de **string**. </br>
Elle publie le Tweet grâce correspondant et change la photo de profil selon la météo grâce aux fonctions précédentes. </br>
Elle affiche un message de log lorsque le Tweet est publié (dans la console et dans le fichier [main.log](https://github.com/Timoleroux/Weather-Bot/blob/main/main.log))</br>
Si l'opération réussit elle retourne `True`.

### main.py/makeSchedulesValid

    makeSchedulesValid()
    Input : ['8h', '12:30', '25h30']
    Output : ['08h00', '12h30']

Cette fonction prend en entée une liste d'horaires.
Elle formate les horaires de manière conforme pour pouvoir être lu par [main.py](#mainpyautorun)
Elle retourne la liste d'horaires formatée et si cette liste est vide, elle retourne `False`.

### main.py/autoRun

    autoRun()
    Input : ['08h00', '12h00', '20h30']
    Output : None

Cette fonction prend entrée une ville sous forme de **string** et une liste d'horaires. </br>
Grâce à la fonction précédente, elle formate correctement la liste d'horaire et s'il n'y en a aucun valide, elle retourne `False`.
Ensuite, chaque jour, pour chacun des horaires de la liste, elle publie le tweet contenant la météo correspondant à la ville choisie.</br>
Puis elle affiche un message de log lorsque le Tweet est publié (dans la console et dans le fichier [main.log](https://github.com/Timoleroux/Weather-Bot/blob/main/main.log))</br>

---
## Documentation des erreurs communes

La plupart du temps, l'erreur suivante est causée par les tokens écrits dans le fichier [ressources.py](https://github.com/Timoleroux/Weather-Bot/blob/main/ressources.py) qui sont incorrects.

    tweepy.errors.Unauthorized: 401 Unauthorized
    32 - Could not authenticate you.

Si vous obtenez l'erreur suivante, c'est que le Tweet que vous essayez de publier existe déjà.

    tweepy.errors.Forbidden: 403 Forbidden
    187 - Status is a duplicate.

Souvent, l'erreur suivante est due au nom de la ville qui n'est pas valide.

    pyowm.commons.exceptions.NotFoundError: Unable to find the resource

En général, ce genre d'erreur est due à un programme externe (du type antivirus) qui bloque les connexions avec les modules.

    pyowm.commons.exceptions.InvalidSSLCertificateError:
