#!/usr/bin/env python
# -*- coding: utf-8  -*-

import requests
import os
import unicodedata
import re
import json
import sys
sys.path.append("..")
from utils import *

srcdir =  os.path.abspath(os.path.join("..", "src", "zohar"))
datadir = os.path.join("..", "data")
if not os.path.exists(datadir):
	os.makedirs(datadir)

def fix(text):
	text = re.sub("\<[^>]+\>", "", text)
	text = re.sub('\(ס\י" [^)]+\)', "", text)
	text = re.sub('\(ס\"א [^)]+\)', "", text)
	text = re.sub('\(נ\"א [^)]+\)', "", text)
	text = re.sub("(\([^)]+\))", r" \1", text)
	text = re.sub("\([^)]+\)", "", text) #TEMP
	text = re.sub("[(\)]", "", text)
	text = re.sub("[ ]+", " ", text)
	text = text.replace("'", "׳").replace('"', "״")
	text = text.replace("\u005c", "").replace("1", "").replace("2", "").replace("3", "")
	text = text.replace("[", "").replace("]", "")
	text = text.replace("יְיָ", "יהוה")
	text = strip_punctuation(text)
	return text

def import_zohar():
	jsonfile = os.path.join(srcdir, "zohar.json")
	data = json.load(open(jsonfile))["text"]

	out = []
	for name in list(data.keys())[:52]: #TODO: addendums
		chapter_number, chapter_name = name.split("_")
		co = []
		for ak, aline in data[name].items():
			ao = []
			for pk, text in data[name][ak].items():
				text = fix(text)
				ao.append(text)
			co.append(ao)
		out.append(co)
	open(os.path.join(datadir, "zohar.json"), "w").write(json.dumps(out, ensure_ascii=False, indent=""))

import_zohar()

