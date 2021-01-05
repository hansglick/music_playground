# Overview

Repository d'un bac à sable lié à la musique electronique et à la data science. Développement de plusieurs applications liées à la musique éléctronique. En vrac : extraction de la discographie d'un artiste, téléchargement de la discographie d'un artiste au format mp3, extraction des features audio d'un fichier mp3, clustering des tracks basés sur des features audio, évolution de la musique éléctro sur les dernières décénies basée sur les features audio, génération de morceaux d'après le style d'un artiste via des modèles deep learning, etc.


<img src="img/djhp.PNG" width="622">


# Environnement Python

Afin d'utiliser les applications, on doit installer l'environnement adéquat. Pour ce faire, utilisez conda avec les commandes suivantes :
```
git clone https://github.com/hansglick/music_playground.git
conda env create -f environment.yml
conda activate music
```

# Applications

### **Extraction des tracks d'un artiste**

L'application [app_grab_tracks](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber.py) permet d'extraire l'ensemble des tracks (et leurs [meta data](https://github.com/hansglick/music_playground/blob/master/img/trackdata.PNG)) d'un artiste sous la forme d'un json. Lancez les commandes suivantes afin d'extraire la discographie de *James Ruskin* :

```
cd app_grab_tracks
conda activate music
(music) python grabber.py -a james ruskin -f tracks.json
```

 * **-a** : le nom de l'artiste
 * **-f** : le nom du json qui contiendra les résultats, i.e. la [discographie](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/tracks.json) de l'artiste


### **Mise à jour du json discographie**

L'application [grabber_all.py](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber_all.py) permet de mettre un jour un fichier json discographies qui comprend tout les tracks d'un set d'artistes. Lancez les commandes ci-dessous pour rajouter les tracks des artistes *Eyal Golan* et *Laurent Garnier* ([artistes.txt](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt)) au fichier discographie  `trackslist/tracks.json` :

```
cd app_grab_tracks
conda activate music
(music) python grabber_all.py -a artists.txt -f trackslist/tracks.json
```

 * **-a** : un fichier qui comprend les artistes pour lesquels on veut rajouter les tracks au fichier json discographie. Voir le [format](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt) 
 * **-f** : le nom du json qui fait office de discographies. Comprend toutes les discographies. Ce fichier est mis à jour avec les nouveaux artistes présents dans le fichier qui fait office d'input `-a`