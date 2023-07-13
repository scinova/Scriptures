#!/usr/bin/env python
# -*- coding: utf-8  -*-

import csv
import json
import os
import requests

import sys
sys.path.append("..")
srcfolder = os.path.join("..", "src", "talmud")
if not os.path.exists(srcfolder):
	os.makedirs(srcfolder)

import Talmud
talmud = Talmud.Talmud()

def download_talmud():
#	tractates = csv.reader(open("tractates.csv"), delimiter=" ", quotechar='"')
#	for tractate_nr, (order_nr, name, latin_name, num_pages) in enumerate(tractates, start=1):
	for tractate in talmud.tractates:
		#order_nr = int(order_nr)
		#print (tractate_nr, latin_name)
		suffix = "Vocalized Aramaic"
		if tractate.latin_name == 'Pesachim':
			suffix = "Vocalized Punctuated Aramaic"
		if tractate.order.number == 4 and tractate.latin_name != 'Bava Batra': #Nezikin
			suffix = "Aramaic"
		if tractate.order.number == 5 and tractate.latin_name != 'Meilah': #Kodashim
			suffix = "Aramaic"
		if tractate.latin_name == 'Niddah':
			suffix = "Aramaic"
		filename = '%02d.json'%tractate.number
		url = "https://www.sefaria.org.il/download/version/%s - he - William Davidson Edition - %s.json"%(tractate.latin_name, suffix)
		print (url)
		r = requests.get(url)
		if r.status_code == 200:
			folder = os.path.join(srcfolder, "sefaria")
			if not os.path.exists(folder):
				os.makedirs(folder)
			open(os.path.join(folder, filename), 'w').write(r.text)
		else:
			print (r.status_code)
		url = "https://www.sefaria.org.il/download/version/%s - he - Wikisource Talmud Bavli.json"%(tractate.latin_name)
		print (url)
		r = requests.get(url)
		if r.status_code == 200:
			folder = os.path.join(srcfolder, "wikisource")
			if not os.path.exists(folder):
				os.makedirs(folder)
			open(os.path.join(folder, filename), 'w').write(r.text)
		else:
			print (r.status_code)

download_talmud()
