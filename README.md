# Overview

Repository du bac à sable music. Développement de plusieurs applications liées à la musique éléctronique.


# Applications

### **Cloner et installer l'environnement conda**

Afin d'utiliser les applications, on doit installer l'environnement adéquat. Pour ce faire, utilisez conda avec les commandes suivantes :
```
git clone https://github.com/hansglick/adth-tt.git
conda env create -f environment.yml
conda activate music
```

### ** Extraction des tracks d'un artiste **

[grabber.py](https://github.com/hansglick/music_playground/blob/master/grabber.py) : permet d'extraire l'ensemble des tracks d'un artiste sous la forme d'un json. Peut prendre plusieurs minutes selon la carrière de l'artiste

```
conda activate music
(music) python grab_trakcs/grabber.py -a laurent garnier >> tracks.json
```