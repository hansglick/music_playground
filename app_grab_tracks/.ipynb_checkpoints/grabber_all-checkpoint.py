import subprocess
import json
import os.path
import argparse
import sys



# HARDCODED PARAMETERS
directory = "/home/osboxes/proj/music_playground/app_grab_tracks/"
which_python = "/home/osboxes/anaconda3/envs/music/bin/python"



def update_tracks_file(args):



	# EXTRACT ARGUMENTS
	artists_filename = args.artists_filename
	tracks_filename = args.tracks_filename


	requested_artists = []
	with open(artists_filename) as file:
		for l in file:
			requested_artists.append(l.strip())

	# PATH FILENAME
	saved_tracks_filename = directory + tracks_filename


	# EXISTE-T-IL?
	if os.path.isfile(saved_tracks_filename):
		file_exist = True
	else:
		file_exist = False


	# DEFINITION DES CLEAN REQUESTS ARTISTS ET TRACKS
	if file_exist:
		with open(saved_tracks_filename) as json_file: 
			tracks = json.load(json_file) 
		saved_artists = list(set([item["artist"] for item in tracks]))    
		cleaned_requested_artists = [artist for artist in requested_artists if artist not in saved_artists]
		
	else:
		tracks = []
		cleaned_requested_artists = requested_artists


	# DEFINITION DES COMMANDES BASH
	commandbashes = [which_python + " " + directory + "grabber.py -a " + requested_artist + " -f " + directory + "trackslist/temp.json" for requested_artist in cleaned_requested_artists]


	# RUN LES BASH ET APPEND LES RESULTS
	for commandbash in commandbashes:
		print(commandbash)
		cp = subprocess.run([commandbash],shell = True, capture_output = True)
		with open(directory + "trackslist/temp.json") as json_file: 
			temp_tracks = json.load(json_file)
		tracks = tracks+temp_tracks


	# SAVE JSON FILE
	print("Save results in json file")
	with open(saved_tracks_filename, 'w') as outfile:
		json.dump(tracks, outfile)


	return None








if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='test arguments')
	parser.add_argument('-a', '--artists_filename')
	parser.add_argument('-f','--tracks_filename')
	args = parser.parse_args()
	update_tracks_file(args)