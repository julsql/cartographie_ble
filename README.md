# NET4104 - Internet sans fil : concepts, technologies et architectures

* Gabriel Lima
* Théo Lardeur
* Juliette Debono

## Cartographie des appareils BLE

Le but de notre projet et d'obtenir les appareils détéctables (identifié par leur adresse mac) par notre ESP32-S3 chercheuse, ainsi que les appareils détéctables par les ESP voisines de notre ESP et d'en faire une représentation sous forme d'un arbre.

## Utiliser le programme

Se connecter au terminal de toutes les ESP à utiliser. Seulement une ESP chercheuse en même temps.

Sur toutes les ESP qui servent de relais lancer le fichier python [receiver.py](./receiver.py) (ATTENTION il faut également mettre le fichier [values.py](./values.py))

Sur l'ESP chercheuse (la principale), on lance le fichier python [searcher.py](./searcher.py) (ATTENTION il faut également mettre le fichier [values.py](./values.py)). L'arbre des adresses mac des voisins va être print dans le terminal de l'ESP chercheuse.

Durant leur fonctionnement, les ESP relais vont être en bleues, tandis que l'ESP chercheuse va être en vert.

Plus facile :

* run le fichier [receiver.sh](./receiver.sh) en modifiant le port à celui des ESP qui servent de relais.
* run le fichier [searcher.sh](./searcher.sh) en modifiant le port à celui de l'ESP chercheuse.
* boot d'abord toutes les ESP relais, puis l'EPS chercheuse qui va lancer sa recherche (le resultat est print dans le terminal, s'assurer de l'avoir ouvert)