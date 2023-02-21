# NET4104 - Internet sans fil : concepts, technologies et architectures
Gabriel Lima
Théo Lardeur
Juliette Debono

## Cartographie des appareils BLE

Le but de notre projet et d'obtenir les appareils détéctables par notre ESP32-S3, ainsi que les appareils détéctables par les appreils que nous avons trouvé etc… et d'en faire une représentation.
Possibilité d'afficher cette représentation via un [serveur web](https://gcworks.fr/tutoriel/esp/Serveurweb.html)

# Programmer sa ESP32-S3 avec MicroPython
[Installation de MicroPython](https://micropython.org/download/GENERIC_S3/)
[Bibliotheques MicroPython](https://github.com/micropython/micropython-lib)

Brancher la carte sur le port UART

## Connaître son port :

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

## Executer notre fichier

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