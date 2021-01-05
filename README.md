# Overview

Repository du bac à sable music. Développement de plusieurs applications liées à la musique éléctronique.

# Environnement Python

Afin d'utiliser les applications, on doit installer l'environnement adéquat. Pour ce faire, utilisez conda avec les commandes suivantes :
```
git clone https://github.com/hansglick/music_playground.git
conda env create -f environment.yml
conda activate music
```

# Applications

### **Extraction des tracks d'un artiste**

L'application ***grab_tracks*** permet d'extraire l'ensemble des tracks d'un artiste sous la forme d'un json. Comme, l'illustre l'image c-dessous, les informations récupérées sont très divers : nom, date, album/compil, features audio, etc. Les arguments de l'applicatio sont les suivants : 
 * **-a** : le nom de l'artiste
 * **-f** : le filename de json qui contiendra la discographie de l'artiste
 * [grabber.py](https://github.com/hansglick/music_playground/blob/master/grab_tracks/grabber.py)
 * [notebook](https://github.com/hansglick/music_playground/blob/master/grab_tracks/grabber.ipynb)

```
conda activate music
(music) python grab_trakcs/grabber.py -a james ruskin -f grab_tracks/james_ruskin_tracks.json
```

<img src="img/trackdata.PNG" width="495">



