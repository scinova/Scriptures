#!/usr/bin/env python
# -*- coding: utf-8  -*-

import csv
import hebrew_numbers
import json
import os
import re
from utils import *

root = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(root, "data")
dbdir = os.path.join(root, "db")
f = os.path.join(datadir, "talmud.json")
DATA = json.load(open(f)) if os.path.exists(f) else None

class Texts:
	def __init__(self, paragraph):
		self.paragraph = paragraph

	@property
	def text(self):
		""" pointed gemarah text """
		return DATA[self.paragraph.page.tractate.number - 1][self.paragraph.page.number - 1][self.paragraph.number - 1]

	@property
	def presentation(self):
		return self.text

	@property
	def printed(self):
		""" bare text with abbreviations"""
		return strip_hebrew_points(self.printedpointed)

	@property
	def printedpointed(self):
		text = strip_punctuation(self.presentation).replace('\u2028', ' ').replace('"', '').replace("'", '')
		return text

	@property
	def wikisource(self):
		return ""

	@property
	def rashi(self):
		""" Rashi commentary text """
		return ""

	@property
	def tosafot(self):
		""" Tosafot commentary text """
		return ""

class Paragraph:
	def __init__(self, number, page):
		self.number = number
		self.page = page
		self.texts = Texts(self)

	@property
	def hebrew_number(self):
		return hebrew_numbers.int_to_gematria(self.number, gershayim=False)

class Page:
	def __init__(self, number, tractate):
		self.number = number
		idx = number - 1
		self.folio = int(idx  / 2) + 2
		self.side = 'b' if idx % 2 else 'a'
		self.tractate = tractate
		self.paragraphs = []

	@property
	def hebrew_number(self):
		return '%s%s'%(hebrew_numbers.int_to_gematria(self.folio, gershayim=False), '.' if self.side == 'a' else ':')

	def __repr__(self):
		return '<Page %03d%s (%s)>'%(self.folio, self.side, self.tractate.latin_name)

class Section:
	def __init__(self, chapter):
		self.chapter = chapter
		self.verses = []

	@property
	def pages(self):
		return sorted(list(set([verse.page for verse in self.verses])), key=lambda x: x.hebrew_number)

	@property
	def number(self):
		return self.chapter.sections.index(self) + 1

	@property
	def name(self):
		return ' '.join(self.verses[0].srctextclean.split(' ')[1:3])

class Chapter:
	def __init__(self, tractate, name=''):
		self.tractate = tractate
		self.verses = []
		self.sections = []
		self.name = name

	@property
	def pages(self):
		return sorted(list(set([verse.page for verse in self.verses])), key=lambda x: x.hebrew_number)

	@property
	def number(self):
		return self.tractate.chapters.index(self) + 1

class Article:
	def __init__(self, tractate, folio, side, start, length):
		self.tractate = tractate
		self.verses = []
		s = False
		for verse in self.tractate.verses:
			if verse.page.folio == folio and verse.page.side == side and verse.number == start:
				s = True
			if s and len(self.verses) < length:
				self.verses.append(verse)

	@property
	def number(self):
		return self.tractate.articles.index(self) + 1

	@property
	def words(self):
		return [word for verse in self.verses for word in verse.words]

class Tractate:
	def __init__(self, number, order, name, latin_name):
		self.number = number
		self.order = order
		self.name = name
		self.latin_name = latin_name
		self.pages = []
#		self.chapters = []
#		self.articles = []

class Order:
	def __init__(self, number, name, latin_name):
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.tractates = []

class Talmud:
	def __init__(self):
		print ("talmud.init")
		self.orders = []
		lines = csv.reader(open(os.path.join(dbdir, "orders.csv")), delimiter=" ", quotechar='"')
		for order_nr, (name, latin_name) in enumerate(lines, start=1):
			order = Order(order_nr, name, latin_name)
			self.orders.append(order)
		self.tractates = []
		lines = csv.reader(open(os.path.join(dbdir, "tractates.csv")), delimiter=" ", quotechar='"')
		for tractate_nr, (order_nr, name, latin_name, num_pages) in enumerate(lines, start=1):
			order = self.orders[int(order_nr) - 1]
			tractate = Tractate(tractate_nr, order, name, latin_name)
			for page_nr in range(1, int(num_pages) + 1):
				page = Page(page_nr, tractate)
				if DATA:
					for paragraph_nr, _ in enumerate(DATA[tractate.number - 1][page.number - 1], start=1):
						page.paragraphs.append(Paragraph(paragraph_nr, page))
				tractate.pages.append(page)
			self.tractates.append(tractate)
		print ("talmud.init end")

	@property
	def pages(self):
		return [page for tractate in self.tractates for page in tractate.pages]

	@property
	def paragraphs(self):
		return [paragraph for page in self.pages for paragraph in page.paragraphs]

if __name__ == '__main__':
	talmud = Talmud()
