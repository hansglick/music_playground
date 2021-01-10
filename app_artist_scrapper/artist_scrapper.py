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



driver = webdriver.Chrome(chrome_path)
root_url = "https://ra.co"
graine_app = ["/dj/davidguetta"]
seconds_to_wait = 1


def From_Hosts_Array(targets_array,artist_dic,errors_bac):

	new_targets_names = []
	errors = []
	new_targets_urls = targets_array
	iterator = 0
	for target in targets_array:


		# Printer
		iterator = iterator + 1
		toprint = "\riterator : " + str(iterator) + "/" + str(len(targets_array))
		print(toprint, end="", flush=True)
		

		if target in errors_bac:
			print("Just see an error url")
			continue

		try:

			# On va sur la page de l'host
			driver.get(root_url+target)
			driver.implicitly_wait(seconds_to_wait)

			# On récupère le nom de l'artiste
			elements = driver.find_elements_by_css_selector(".dqXcHH")
			artistname = [el.text for el in elements][0]
			new_targets_names = new_targets_names + [artistname]

			# alias
			elements = driver.find_elements_by_css_selector(".gqevKX")
			artistaliases = [el.text for el in elements]
			
			# .kShwWa le pays
			elements = driver.find_elements_by_css_selector(".kShwWa")
			artistcountry = [el.text for el in elements]

			# .dqnnCL le n abonnés
			elements = driver.find_elements_by_css_selector(".dqnnCL")
			artistfollowers = [el.text for el in elements]

			# dic
			artist_dic[target] = {"url":target,
			"name":artistname,
			"alias":artistaliases,
			"country":artistcountry[0],
			"followers":artistfollowers[0]}

			# On récupère les url relatives des artistes associées
			elements = driver.find_elements_by_css_selector(".bBzkjA .kCKrCv")
			#new_targets_urls = new_targets_urls + [el.get_attribute("href") for el in elements]
			#new_targets_names = new_targets_names + [el.text for el in elements]
			for artisturl,artistname in zip([el.get_attribute("href") for el in elements],[el.text for el in elements]):
				if artisturl[1:7] != "labels":
					new_targets_urls = new_targets_urls + [artisturl]
					new_targets_names = new_targets_names + [artistname]

		except:
			errors.append(root_url+target)
			print("!!!!! ALARM ERROR !!!! ")
			time.sleep(15)
		
	return (new_targets_urls,new_targets_names,artist_dic,errors)


class Crawler:
	
	def __init__(self,graine):

		if not os.path.isfile("bac.pkl"):
			print("pas de Loadder, initialisation")
			self.bac = graine
			self.runs = 0
			self.artists_names = []
			self.artists_urls = []
			self.artist_dic = {}
			self.errors = []
		else:
			print("Loadder run!")
			self.Loadder()

	def Loadder(self):
		self.bac = pickle.load(open('bac.pkl', 'rb'))
		self.runs = pickle.load(open('runs.pkl', 'rb'))
		self.artist_dic = pickle.load(open('artist_dic.pkl', 'rb'))
		self.artists_names = pickle.load(open('artists_names.pkl', 'rb'))
		self.artists_urls = pickle.load(open('artists_urls.pkl', 'rb'))
		self.errors = pickle.load(open('errors.pkl', 'rb'))

	def Explore(self):
		while(len(self.bac)>0):
			self.Run()

	def Run(self,verbose = True):
		
		# Assignements
		new_targets_urls,new_targets_names,self.artist_dic,errors = From_Hosts_Array(self.bac,self.artist_dic,self.errors)
		
		print("")
		print("ERRORS")
		print(errors)
		print(self.errors)
		print("")

		self.bac = [item for item in new_targets_urls if item not in self.artists_urls]
		self.artists_names = list(set(self.artists_names + new_targets_names))
		self.artists_urls = list(set(self.artists_urls + new_targets_urls))
		self.runs = self.runs + 1
		self.errors = self.errors + errors
		self.bac = self.bac + errors
		self.bac = list(set(self.bac))

		# Save the object
		pickle.dump(self.bac, open('bac.pkl', 'wb'))
		pickle.dump(self.artist_dic, open('artist_dic.pkl', 'wb'))
		pickle.dump(self.artists_names, open('artists_names.pkl', 'wb'))
		pickle.dump(self.artists_urls, open('artists_urls.pkl', 'wb'))
		pickle.dump(self.runs, open('runs.pkl', 'wb'))
		pickle.dump(self.errors, open('errors.pkl', 'wb'))

		# Saved artist_dic as a json file
		with open("artists.json", 'w') as outfile:
			json.dump(self.artist_dic, outfile,indent=4, sort_keys=True)

		# Printer
		if verbose:
			print("")
			print("runs : ", str(self.runs))
			#print("")
			print("errors : ", str(len(self.errors)))
			#print("")
			#print("bac")
			print("taille du bac : ",str(len(self.bac)))
			#print("bac : ", self.bac)
			#print("")
			#print("artists_names")
			print("taille de artists names : ",str(len(self.artists_names)))
			#print(self.artists_names)
			#print("")
			#print("artists_urls")
			print("taille de artists urls : ",str(len(self.artists_urls)))
			#print(self.artists_urls)
			#print("")
			print("taille du dic : ", str(len(self.artist_dic)))
			#print(self.artist_dic)
			
			print("")
			print("")
			print("")


			
mycrawler = Crawler(graine_app)
mycrawler.Explore()






