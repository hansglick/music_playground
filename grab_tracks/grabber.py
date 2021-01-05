import argparse
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm_notebook
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from fun import *

def extract_tracks(args):
	artists_list = " ".join(args.artist)
	print(artists_list)
	artists_data = artist_all_tracks(artists_list)
	artists_df = df_tracks(artists_data)
	results = artists_df.to_dict(orient="records")
	return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test arguments')
    parser.add_argument('-a', '--artist', nargs='+', default=[])
    args = parser.parse_args()
    extract_tracks(args)