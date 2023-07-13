#!/usr/bin/env python
# -*- coding: utf-8  -*-

import Tanakh
import Talmud
import Zohar
import os
import re
from utils import *

def makedict(words):
	d = {}
	for word in words:
		bareword = strip_hebrew_points(word)
		if not bareword in d:
			d[bareword] = []
		d[bareword].append(word)
	return d

class Scriptures(object):
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Scriptures, cls).__new__(cls)
		return cls.instance

	def __init__(self):
		self.tanakh = Tanakh.Tanakh()
		self.pentateuch = self.tanakh.pentateuch
		self.prophets = self.tanakh.prophets
		self.writings = self.tanakh.writings
		self.talmud = Talmud.Talmud()
		self.zohar = Zohar.Zohar()

		self.onkelos_words = sorted(list(set(self.onkelos_allwords)))
		self.jerusalmi_words = sorted(list(set(self.jerusalmi_allwords)))
		self.jonathan_words = sorted(list(set(self.jonathan_allwords)))
		self.targum_words = sorted(list(set(self.targum_allwords)))
		self.talmud_words = sorted(list(set(self.talmud_allwords)))
		self.zohar_words = sorted(list(set(self.zohar_allwords)))

		self.onkelos_dictionary = makedict(self.onkelos_words)
		self.jerusalmi_dictionary = makedict(self.jerusalmi_words)
		self.jonathan_dictionary = makedict(self.jonathan_words)
		self.targum_dictionary = makedict(self.targum_words)
		self.talmud_dictionary = makedict(self.talmud_words)
		self.zohar_dictionary = makedict(self.zohar_words)

	@property
	def onkelos_allwords(self):
		return [word for verse in self.pentateuch.verses for word in verse.texts.onkelos.split(" ")]

	@property
	def jerusalmi_allwords(self):
		return [word for verse in self.pentateuch.verses for word in verse.texts.jerusalmi.split(" ")]

	@property
	def jonathan_allwords(self):
		return [word for verse in self.prophets.verses for word in verse.texts.jonathan.split(" ")]

	@property
	def targum_allwords(self):
		return [word for verse in self.writings.verses if verse.chapter.book.number < 35 for word in verse.texts.targum.split(" ")]

	@property
	def talmud_allwords(self):
		return [word for paragraph in self.talmud.paragraphs for word in paragraph.texts.text.split(" ")]


	@property
	def zohar_allwords(self):
		return [word for paragraph in self.zohar.paragraphs for word in paragraph.texts.text.split(" ")]


if __name__ == "__main__":
	scriptures = Scriptures()
