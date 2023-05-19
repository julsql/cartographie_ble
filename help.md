# AIDE

Aide mémoire pour la programmation avec micropython (doc, trouver le port, ajouter et run des fichiers…) configuer l'ESP pour faire marcher micropython.

## Programmer sa ESP32-S3 avec MicroPython

[Installation de MicroPython](https://micropython.org/download/GENERIC_S3/)
[Bibliotheques MicroPython](https://github.com/micropython/micropython-lib)

Brancher la carte sur le port UART

## Connaître son port

[Trouver le port](https://docs.espressif.com/projects/esp-idf/en/v4.4-beta1/esp32/get-started/establish-serial-connection.html)

Ports sur Mac :

    /dev/cu.usbserial-XXXX

Ports sur Linux :

    /dev/ttyXXXX

Ports sur Windows :

    COMX

Trouver le port (Mac & Linux):

Exécuter avant et apès avoir connecté ESP32 pour voir le port en plus :

> Sur Mac :

    ls /dev/cu.*

> Sur Linux

    ls /dev/tty*

> Sur Windows

Chercher les ports dans le Windows Device Manager

## Installer MicroPython sur la ESP32-S3

Installer le programme esptool.py

Télécharger : [GENERIC_S3-20220618-v1.19.1.bin](https://micropython.org/resources/firmware/GENERIC_S3-20220618-v1.19.1.bin)

Exécuter les commandes suivantes :

    esptool.py --chip esp32s3 --port <port> erase_flash
    esptool.py --chip esp32s3 --port <port> write_flash -z 0 GENERIC_S3-20220618-v1.19.1.bin

## Utiliser Python

Créer un fichier python et le déplacer dans ESP32-S3 :

Installer ampy

    pip install adafruit-ampy

Déplacer fichier
> Attention : Il faut que toutes les connexions avec ESP32-S3 soient fermées sinon il y aura une erreur !

    ampy --port <port> put main.py

Se connecter via terminal :

    screen <port> 115200

Trouver les connexions actives :

    lsof | grep usbserial

## Exécuter notre fichier

- On modifie notre fichier python (ex : main.py)

- On le déplace dans la ESP32-S3 (Attention à bien stopper toutes les connexions avec la ESP32 avant, sinon la débrancher)

        ampy --port <port> put main.py

- On Lance la connexion avec la ESP32 et on arrive sur un terminal python

- On peut donc executer du python, par exemple le fichier qu'on a déplacé :

        >>> import main

## Scanner les appareils : Installation de Aioble

> [Aioble](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble)

    pip install mpremote
    pip install mip

    mpremote connect <port> mip install aioble

## Git - Utilisation

Se connecter à [https://gitlabens.imtbs-tsp.eu](https://gitlabens.imtbs-tsp.eu) via Shibboleth avec ses identifiants de l’école
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
