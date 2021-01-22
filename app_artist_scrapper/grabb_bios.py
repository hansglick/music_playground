from selenium import webdriver
import getpass
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from conf import *
import pyautogui
import pandas as pd
import pickle
import os.path
import time
import json
import sys

# 0. DEFINE SCRAPPER VARIABLES
driver = webdriver.Chrome(chrome_path)
root_url = "https://ra.co"
seconds_to_wait = 5

# LOAD DATA
# 1.
with open('artists.json') as json_file:
	artists = json.load(json_file)
# 2.
if not os.path.isfile("biographies.json"):
	biographies = {}
else:
	with open('biographies.json') as json_file:
		biographies = json.load(json_file)
# 3.
if not os.path.isfile("other.json"):
	other = {"urls_seen":[],"urls_errors":[],"urls_good":[]}
else:
	with open('other.json') as json_file:
		other = json.load(json_file)


class BioGrabber:



	def __init__(self,artists,biographies,other):

		"""
		Méthode d'initialisation d'un objet BioGrabber.
		Joue principalement la fonction d'un data loadder.
		"""
		
		self.biographies = biographies
		self.artists = artists
		self.urls_seen = other["urls_seen"]
		self.urls_errors = other["urls_errors"]
		self.urls_good = other["urls_good"]

		#
		biomemory = round((sys.getsizeof(self.biographies) / 1000000),1)
		self.biomemory = str(biomemory) + " Mo"



	def Saver(self):

		"""
		Méthode qui sauve les fichiers.
		Appelée toutes les 25 biographies sauvegardées.
		Sauvegarde les fichiers other.json (progression du scrapping) et biographies.json (les biographies des artistes)
		"""

		#
		biomemory = round((sys.getsizeof(self.biographies) / 1000000),1)
		self.biomemory = str(biomemory) + " Mo"
		
		print("Save biographies.json")
		with open("biographies.json", 'w') as outfile:
			json.dump(self.biographies, outfile,indent=4, sort_keys=True)

		print("Save other.json")
		print("")
		other = {"urls_seen":self.urls_seen,"urls_errors":self.urls_errors,"urls_good":self.urls_good}
		with open("other.json", 'w') as outfile:
			json.dump(other, outfile,indent=4, sort_keys=True)



	def Grab(self):

		"""
		Méthode principale de l'objet BioGrabber.
		Pour chaque artiste de qui il n'a pas encore téléchargé la bio, il va télécharger la bio.
		Toutes les 25 biographies téléchargées le scrapping s'arrête pour effectuer une sauvegarde.
		"""

		for artistkey, artistobj in artists.items():

			if artistkey not in self.urls_seen:

				artist_name = artistobj["name"]
				artist_url = artistobj["url"]
				bio_url = root_url + artist_url + "/biography"

				print("URLS Scannées :",len(self.urls_seen))
				print("URLS Errors :",len(self.urls_errors))
				print("Biographies Enregistrées :",len(self.urls_good),"(",self.biomemory,")")
				print("URLS Restantes :", len(artists)-len(self.urls_seen))
				print("Grabbing :",artist_name,"(",bio_url,")")
				print("")
				
				try:
					driver.get(bio_url)
					driver.implicitly_wait(seconds_to_wait)
					elements = driver.find_elements_by_css_selector(".eYivkC")
					bio_elements = [el.text for el in elements]
					biography = "\n".join(bio_elements)
					self.biographies[artist_url] = biography
					self.urls_seen.append(artist_url)
					self.urls_good.append(artist_url)
				except:
					self.urls_errors.append(artist_url)
					self.urls_seen.append(artist_url)


				if len(self.urls_good)%25 == 0:
					self.Saver()





mybiograbber = BioGrabber(artists,biographies,other)
mybiograbber.Grab()




