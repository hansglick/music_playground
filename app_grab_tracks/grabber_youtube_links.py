from youtube_search import YoutubeSearch
import json
import argparse
import sys

def update_tracks_with_urls(args):

	
	# IMPORTATION DES DISCOGRAPHIES
	tracks_filename = args.tracks_filename
	with open(tracks_filename) as json_file: 
		tracks = json.load(json_file)


	# FIND URLS
	for iditem,item in enumerate(tracks):

		if "youtube" not in item:

			artist = item["artist_str"]
			songname = item["name"]
			request = artist + " - " + songname
			search_results = YoutubeSearch(request, max_results=1).to_dict()
			item["youtube"] = search_results

			try:
				pct = round(((iditem+1)/len(tracks)),2) * 100
				pct = str(pct)+"%"
				to_print_a = "counter : " + str(iditem + 1) + "/" + str(len(tracks)) 
				to_print_b = "progression : " + pct
				to_print_c = request
				duration = search_results[0]["duration"]
				views = search_results[0]["views"]
				to_print_d = views + ", " + duration
				to_print = to_print_a + " | " + to_print_b + " | " + to_print_c + " | " + to_print_d
				print(to_print)
			except:
				to_print = "Cannot print, problem!" + to_print_a + " | " + to_print_b
				print(to_print)

	# SAVE DISCOGRAPHIES
	print("Saving results in discographies json")
	with open(tracks_filename, 'w') as outfile:
		json.dump(tracks, outfile)

	

	return None







if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='test arguments')
	parser.add_argument('-f','--tracks_filename')
	args = parser.parse_args()
	update_tracks_with_urls(args)