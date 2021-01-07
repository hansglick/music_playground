from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
from tqdm import tqdm_notebook
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = '468641629111454b95f33e0be7eb09a2'
client_secret = 'b918bb0cd7dc4e7e925decce5b229710'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def Get_Artist_Id(artist_name):
   
    """
    Renvoie le spotify artist uri à partir du nom d'un artiste
    """
   
    artist_uri = sp.search(artist_name)['tracks']['items'][0]['artists'][0]['uri']
    artist_str = sp.search(artist_name)['tracks']['items'][0]['artists'][0]["name"]
   
    return artist_uri,artist_str


def Get_Potential_Tracks(artist_uri):
   
    """
    Renvoie tout les tracks succeptibles de provenir d'un artiste
    On rajoute un item albumid
    """
   
    n = 0
    tracks_objects = []
   
    while True:
        
        print("Exploring pages : ",str(n))
        
        albums_objects = sp.artist_albums(artist_uri,limit = 50,offset = n)
        cdt = len(sp.artist_albums(artist_uri,limit=50, offset = n)['items']) > 0
        if not cdt:
            break
       
        albums_ids = [(album["uri"],album["name"],album["album_type"]) for album in albums_objects["items"]]
        
        for albumid,albumname,albumtype in albums_ids:
            
            temptracks = sp.album_tracks(albumid)["items"]
            
            for track in temptracks:
                track["album"] = {"uri":albumid,"name":albumname,"type":albumtype}
            tracks_objects = tracks_objects + temptracks
           
        n = n +50

    return tracks_objects



def Clean_Potential_Tracks(tracks_objects,artist_uri,artist_str,verbose=True):
   
    """
    A partir d'une liste de tracks objects,
    On renvoie les tracks dont l'auteur est l'artiste
    """
   
    cleaned_tracks_objects = []
    print("Browsing Tracks ...")
    for idtrackobj,trackobj in enumerate(tracks_objects):
        
        # TO PRINT
        if verbose:
            toprint = "\r" + str(idtrackobj + 1) + "/" + str(len(tracks_objects))
            print(toprint,end="",flush=True)
        
        track_artists_ids = [(item["uri"],item["name"]) for item in trackobj["artists"]]
        #print(track_artists_ids)
        #track_artists_ids = [item["uri"] for item in trackobj["artists"]]

        if artist_uri in [item[0] for item in track_artists_ids]:
            trackuri = trackobj["uri"]
            audiofeatures= sp.audio_features(trackuri)[0]
            featuring_ids = [item for item in track_artists_ids if item[0] != artist_uri]
            #featuring_ids = [item for item in track_artists_ids if item != artist_uri]
            track_informations = {"artist":artist_uri,
                                  "artist_str" : artist_str,
                                  "featuring":featuring_ids,
                                  "piste":trackobj["track_number"],
                                  "album":trackobj["album"],
                                  "duration":trackobj["duration_ms"],
                                  "name":trackobj["name"],
                                  "track":trackuri,
                                  "features":audiofeatures}
           
            cleaned_tracks_objects.append(track_informations)
   
    return cleaned_tracks_objects



def Retrieve_Artist_Discography(artist_name):
   
    """
    Renvoie un JSON qui représente la discographie d'un artiste
    """
   
    artist_uri = Get_Artist_Id(artist_name)
    tracks_objects = Get_Potential_Tracks(artist_uri)
    discography = Clean_Potential_Tracks(tracks_objects,artist_uri)
   
    return discography

