# Git - Utilisation

Se connecter à https://gitlabens.imtbs-tsp.eu via Shibboleth avec ses identifiants de l’école
Configurer son compte git avec une clé SSH relié à son ordinateur [détaillé ici](https://gitlabens.imtbs-tsp.eu/help/user/ssh.md).

Nom du dépôt git du projet : cartographie_ble

Si tout est bien configuré, il faut cloner le dépôt git pour récupérer le projet sur l'ordinateur : 

    git clone git@gitlabens.imtbs-tsp.eu:juliette.debono/cartographie_ble.git

Une fois que c’est fait le projet apparaît dans les fichiers de l'ordinateur dans un nouveau dossier : cartographie_ble contenant un main.py, et un README.md avec toutes les incrustions du projet.

Pour mettre à jour ses propre modifications locales disponibles à tout le monde :

    git add *
    git commit -m "nom du commit"
    git push origin

Mettre à jour son dossier local avec les modifications des autres :

    git pull

Autres commandes utiles :

Voir l’état des modifications :

    git status

Voir l’état du dépôt :

    git fetch
