# Weather Bot

Weather Bot est un **bot codé entièrement en python** qui permet de **poster des tweets** annonçant la **météo** de n'importe quelle ville. On peut également programmer un **emploi du temps** où chaque jour, un tweet se postera aux heures prédéfinies.


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
