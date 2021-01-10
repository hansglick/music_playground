# Overview

Repository d'un bac à sable lié à la musique electronique et à la data science. Développement de plusieurs applications liées à la musique éléctronique. En vrac : extraction de la discographie d'un artiste, téléchargement de la discographie d'un artiste au format mp3, extraction des features audio d'un fichier mp3, clustering des tracks basés sur des features audio, évolution de la musique éléctro sur les dernières décénies basée sur les features audio, génération de morceaux d'après le style d'un artiste via des modèles deep learning, etc.


<img src="img/djhp.PNG" width="622">


# Environnement(s) Python

Il existe plusieurs environnements conda à utiliser afin de pouvoir lancer les applications. Les commandes suivantes vous permette de créer l'environnement `music` et `lkdn_env`  :
```
git clone https://github.com/hansglick/music_playground.git

conda env create -f environment.yml
conda activate music

conda env create -f environment_scrapper.yml
conda activate lkdn_env
```

# Applications

### **0. Scrapping des artistes electro**

L'application [app_artist_scrapper](https://github.com/hansglick/music_playground/blob/master/app_artist_scrapper/artist_scrapper.py) permet de scrapper les artistes éléctro présent sur le site [resident advisor](https://ra.co/). A partir d'une liste d'urls représentant les fiches des *artistes graines* du scrapper, on récupère un le fichier [artists.json](https://raw.githubusercontent.com/hansglick/music_playground/master/app_artist_scrapper/artists.json)  qui contient l'ensemble des 25,000 et quelques meta data à leur propos. Pour run le scrapper, lancez les commandes suivantes : 

```
cd app_scrapper
conda activate lkdn_env
(lkdn_env) python artist_scrapper.py
```
Afin de modifier les graines du scrapper, modifiez la variable `graine_app` dans le fichier [artist_scrapper.py](https://github.com/hansglick/music_playground/blob/master/app_artist_scrapper/artist_scrapper.py). La graine `[David Guetta]`, devrait néanmoins faire l'affaire. L'application enregistre régulièrement les résultats et si elle est stopée, elle reprend automatiquement là où elle s'était arrêtée, donc pas de problèmes.

***

### **1. Extraction des tracks d'un artiste**

L'application [app_grab_tracks](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber.py) permet d'extraire l'ensemble des tracks (et leurs [meta data](https://github.com/hansglick/music_playground/blob/master/img/trackdata.PNG)) d'un artiste sous la forme d'un json. Lancez les commandes suivantes afin d'extraire la discographie de *James Ruskin* :

```
cd app_grab_tracks
conda activate music
(music) python grabber.py -a james ruskin -f james_ruskin_discographie.json

```

 * **-a** : le nom de l'artiste
 * **-f** : le nom du json qui contiendra les résultats, i.e. la [discographie](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/james_ruskin_discographie.json) de l'artiste


***

### **2. Mise à jour du json discographie**

L'application [grabber_all.py](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber_all.py) permet de mettre à jour un fichier json discographies qui comprend tout les tracks d'un set d'artistes. Lancez les commandes ci-dessous pour rajouter les tracks des artistes *Eyal Golan* et *Laurent Garnier* ([artistes.txt](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt)) au fichier discographie  `trackslist/tracks.json` :

L'application [grabber_all.py](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber_all.py) permet de récupérer les discographies des artistes présents dans un fichier (par exemple : [artistes.txt](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt)). L'application met à jour le fichier [trackslist/tracks.json](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/trackslist/tracks.json) en fonction des artistes rajoutés, i.e. présents dans le fichier [artistes.txt](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt)

```
cd app_grab_tracks
conda activate music
(music) python grabber_all.py -a artists.txt -f trackslist/tracks.json
```

 * **-a** : un fichier qui comprend les artistes pour lesquels on veut rajouter les tracks au fichier `trackslist/tracks.json`. Voir le [format](https://raw.githubusercontent.com/hansglick/music_playground/master/app_grab_tracks/artists.txt) 
 * **-f** : le nom du json qui fait office de discographies. Comprend toutes les discographies. Ce fichier est mis à jour avec les nouveaux artistes présents dans le fichier qui fait office d'input `-a`

***

### **3. Recherche des URLs YouTube de chaque track**

L'application [grabber_youtube_links.py](https://github.com/hansglick/music_playground/blob/master/app_grab_tracks/grabber_youtube_links.py) permet de mettre à jour le json discography `trackslist/tracks.json`, qui représente tout les tracks de tout les artistes. L'application ajoute pour chaque track, une ribambelle d'informations enregistrées sous l'entrée `youtube`. Ces informations comportent entre autres, l'url du morceau sur YouTube.

```
cd app_grab_tracks
conda activate music
(music) python grabber_youtube_links.py -f trackslist/tracks.json
```
 * **-f** : le nom du json qui fait office de discographies. Comprend tout les tracks de tout les artistes. Ce fichier est mis à jour en ajoutant pour chaque entrée, un nouveau dictionnaire comprenant les meta data du 1er résultat retourné par le moteur de recherche de YouTube lorsque la requête est égale à la concaténation de `Artiste` + `TrackName`


# Problemos

### **Le premier résultat d'une recherche YouTube pas toujours pertinent**

Il s'avère que Youtube galère un peu pour renvoyer la vidéo correspondant au track qu'on recherche en première position, la [vidéo suivante](https://www.youtube.com/watch?v=R-LNBZkVaeU&feature=youtu.be&ab_channel=MartinVincelot) est un screen du run de l'application grabber_urls. Chaque ligne correspond au premier résultat du moteur de recherche youtube pour la requête d'un track. Comme tu peux le voir, il ressort très souvent une interview de 01:54:00 avec 29,310 vues pour des tracks différents. Ceci étant pour des artistes plus connus, je pense qu'il ne fait pas cette erreur. Peut-être faut-il élargir la recherche au top 5 résultats ou bien "oublier" ce track pour lequel le résultat retourné a une durée beaucoup trop grande.
