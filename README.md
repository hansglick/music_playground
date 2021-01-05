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

### ** Extraction des tracks d'un artiste **

L'application permet d'extraire l'ensemble des tracks d'un artiste sous la forme d'un json. Peut prendre plusieurs minutes selon la carrière de l'artiste :
 * [grabber.py](https://github.com/hansglick/music_playground/blob/master/grabber.py)

```
conda activate music
(music) python grab_trakcs/grabber.py -a laurent garnier >> tracks.json
```