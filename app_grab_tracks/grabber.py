import argparse
import sys
import json
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm_notebook
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from fun import *

def extract_tracks(args):
	artist_name = [" ".join(args.artist)][0]
	filename = args.filename	
	
	artist_uri,artist_str = Get_Artist_Id(artist_name)
	print(artist_str)
	print("")
	tracks_objects = Get_Potential_Tracks(artist_uri)
	print("")
	discography = Clean_Potential_Tracks(tracks_objects,artist_uri,artist_str)
	print("")
	print("")
	print("Save JSON File")

	with open(filename, 'w') as outfile:
		json.dump(discography, outfile)
	print("")
	print("")
	print("")
	return None


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='test arguments')
	parser.add_argument('-a', '--artist', nargs='+', default=[])
	parser.add_argument('-f','--filename')
	args = parser.parse_args()
	extract_tracks(args)