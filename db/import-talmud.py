#!/usr/bin/env python
# -*- coding: utf-8  -*-

import json
import os
import re
import requests
import sys
sys.path.append("..")
from utils import *
import Talmud

datadir = os.path.abspath(os.path.join("..", "data"))
if not os.path.exists(datadir):
	os.mkdir(datadir)
srcdir = os.path.abspath(os.path.join("..", "src", "talmud", "sefaria"))

talmud = Talmud.Talmud()

def import_talmud():
	fs = []
	for tractate in talmud.tractates:
		ts = []
		filename = os.path.join(srcdir, "%02d.json"%tractate.number)
		data = json.load(open(filename))["text"][2:]
		for page in tractate.pages:
			ps = []
			plines = data[page.number - 1]
			for pline in plines:
				ps.append(pline)
			ts.append(ps)
		fs.append(ts)
	o = json.dumps(fs, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "talmud.json"), "w").write(o)

import_talmud()
