# Overview

Repository du bac à sable music. Développement de plusieurs applications liées à la musique éléctronique.

# Environnement Python

Afin d'utiliser les applications, on doit installer l'environnement adéquat. Pour ce faire, utilisez conda avec les commandes suivantes :
```
git clone https://github.com/hansglick/adth-tt.git
conda env create -f environment.yml
conda activate music
```

# Applications

### **grab_tracks**, Extraction des tracks d'un artiste

L'application permet d'extraire l'ensemble des tracks d'un artiste sous la forme d'un json. Les arguments sont les suivants : 
 * -a : le nom de l'artiste
 * -f : le filename de json qui contiendra la discographie de l'artiste

```
conda activate music
(music) python grab_trakcs/grabber.py -a laurent garnier -f grab_tracks/laurent_garnier_tracks.json
```

 * [grabber.py](https://github.com/hansglick/music_playground/blob/master/grab_tracks/grabber.py)
 * [notebook](https://github.com/hansglick/music_playground/blob/master/grab_tracks/grabber.ipynb)

 