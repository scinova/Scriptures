import json
import hebrew_numbers
import os
from utils import *

root = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(root, "data")
dbdir = os.path.join(root, "db")
DATA = {}
for p in ["mikra", "onkelos", "jerusalmi", "jonathan", "targum", "tafsir"]:
	filename = os.path.join(datadir, "%s.json"%p)
	DATA[p] = json.load(open(filename)) if os.path.exists(filename) else None

class BaseTexts:
	def __init__(self, verse):
		self.verse = verse

	@property
	def mikra(self):
		return DATA["mikra"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

	@property
	def print(self):
		""" bare text without mesorah marks """
		text = self.mikra
		text = strip_hebrew_points(text)
		text = strip_hebrew_accents(text)
		text = strip_hebrew_punctuation(text)
		return text

class PentateuchTexts(BaseTexts):
	def __init__(self, verse):
		super().__init__(verse)

	@property
	def onkelos(self):
		return DATA["onkelos"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

	@property
	def jerusalmi(self):
		return DATA["jerusalmi"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

	@property
	def tafsir(self):
		return DATA["tafsir"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

class ProphetsTexts(BaseTexts):
	def __init__(self, verse):
		super().__init__(verse)

	@property
	def jonathan(self):
		return DATA["jonathan"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

class WritingsTexts(BaseTexts):
	def __init__(self, verse):
		super().__init__(verse)

	@property
	def targum(self):
		return DATA["targum"][self.verse.chapter.book.number - 1][self.verse.chapter.number - 1][self.verse.number - 1]

class Verse:
	def __init__(self, chapter, number):
		self.chapter = chapter
#		self.parashah = parashah
#		self.reading = reading
		self.number = number

	@property
	def texts(self):
		if self.chapter.book in self.chapter.book.root.pentateuch.books:
			return PentateuchTexts(self)
		elif self.chapter.book in self.chapter.book.root.prophets.books:
			return ProphetsTexts(self)
		elif self.chapter.book in self.chapter.book.root.writings.books:
			return WritingsTexts(self)
		else:
			return None
			print ("FUUUUCLLL")

	def __repr__(self):
		return "<Verse %d.%d.%d>"%(self.chapter.book.number, self.chapter.number, self.number)

	@property
	def hebrew_number(self):
		return hebrew_numbers.int_to_gematria(self.number, gershayim=False)

class Chapter:
	def __init__(self, book, number):
		self.book = book
		self.number = number
		self.verses = []

	@property
	def hebrew_number(self):
		return hebrew_numbers.int_to_gematria(self.number, gershayim=False)

class Reading:
	def __init__(self, parashah, number):
		self.parashah = parashah
		self.number = number

	@property
	def verses(self):
		return [verse for verse in self.parashah.verses if verse.reading == self.number]

class Parashah:
	def __init__(self, book, number, name, latin_name):
		self.book = book
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.readings = [Reading(self, i) for i in range(1, 8)]

	@property
	def verses(self):
		return [verse for verse in self.book.verses if verse.parashah == self]

class Book:
	def __init__(self, root, number, name, latin_name):
		self.root = root
		self.number = number
		self.name = name
		self.latin_name = latin_name
		self.chapters = []

	@property
	def verses(self):
		return [verse for chapter in self.chapters for verse in chapter.verses]

#	@property
#	def parashot(self):
#		return [parashah for parashah in self.root.parashot if parashah.book == self]

class BookCollection:
	def __init__(self, root):
		self.root = root
		self.books = []

	@property
	def verses(self):
		return [verse for book in self.books for verse in book.verses]

	@property
	def chapters(self):
		return [chapter for book in self.books for chapter in book.chapters]

class Pentateuch(BookCollection):
	def __init__(self, root):
		super().__init__(root)
		self.books = self.root.books[0:5]

class Prophets(BookCollection):
	def __init__(self, root):
		super().__init__(root)
		self.books = root.books[5:26]

class Writings(BookCollection):
	def __init__(self, root):
		super().__init__(root)
		self.books = root.books[26:]

def makedict(words):
	d = {}
	for word in words:
		bareword = strip_hebrew_points(word)
		if not bareword in d:
			d[bareword] = []
		d[bareword].append(word)
	return d

class Tanakh:
	def __init__(self):
		print ("tanakh.init")
		self.books = []
		j = json.load(open(os.path.join(dbdir, "books.json")))
		for book_number, (latin_name, name, chapters) in enumerate(j, start=1):
			book = Book(self, book_number, name, latin_name)
			for chapter_number, num_verses in enumerate(range(len(chapters)), start=1):
				chapter = Chapter(book, chapter_number)
				if "mikra" in DATA and DATA["mikra"]:
					for i in range(len(DATA["mikra"][book.number - 1][chapter.number - 1])):
						verse = Verse(chapter, i + 1)
						chapter.verses.append(verse)
				book.chapters.append(chapter)
			self.books.append(book)
		self.pentateuch = Pentateuch(self)
		self.prophets = Prophets(self)
		self.writings = Writings(self)
		print ("tanakh.init end")

if __name__ == "__main__":
	t = Tanakh()
