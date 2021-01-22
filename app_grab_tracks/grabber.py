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
	deduplicated_discography = []
	stockage = []

	try:
		artist_uri,artist_str = Get_Artist_Id(artist_name)
		print(artist_str)
		print("")
		tracks_objects = Get_Potential_Tracks(artist_uri)
		print("")
		discography = Clean_Potential_Tracks(tracks_objects,artist_uri,artist_str)
		print("")
		print("")
		print("deduplication")
		# On choisit name au trackid parce que la reuqete youtube ne dépend que du name et pas du trackid de spotify
		for item in discography:
			if item["name"].strip().lower() not in stockage:
				stockage.append(item["name"].strip().lower())
				deduplicated_discography.append(item)

		print("Nombre de tracks :",len(deduplicated_discography))
		print("Save JSON File")
		with open(filename, 'w') as outfile:
			json.dump(deduplicated_discography, outfile,indent=4, sort_keys=True)
		print("")
		print("")
		print("")

	except:
		with open(filename, 'w') as outfile:
			json.dump([{}], outfile,indent=4, sort_keys=True)
		print("Artiste non existant dans la database de spotify")
		print("le json enregistré est vide")

	return None


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='test arguments')
	parser.add_argument('-a', '--artist', nargs='+', default=[])
	parser.add_argument('-f','--filename')
	args = parser.parse_args()
	extract_tracks(args)