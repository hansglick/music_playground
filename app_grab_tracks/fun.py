from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
from tqdm import tqdm_notebook
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = '468641629111454b95f33e0be7eb09a2'
client_secret = 'b918bb0cd7dc4e7e925decce5b229710'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def Get_Artist_Id(artist_name,max_edit_distance=3):
   
    """
    Renvoie le spotify artist uri à partir du nom d'un artiste
    """

    searchobj = sp.search(artist_name)

    L = []
    for track in searchobj["tracks"]["items"]:
        for artist in track["artists"]:
            L.append((artist["name"],artist["uri"]))
    L = list(set(L))

    X = []
    for name,uri in L:
        dis = levenshtein(artist_name.strip().lower(), name.strip().lower())
        X.append((dis,name,uri))

    X.sort(key = lambda a : a[0])

    if len(X)>0:
        
        if X[0][0]>max_edit_distance:
            artist_uri = ""
            artist_str = ""
        else:
            artist_uri = X[0][2]
            artist_str = X[0][1]
    else:
        artist_uri = ""
        artist_str = ""



   
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

