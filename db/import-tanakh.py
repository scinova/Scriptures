#!/usr/bin/env python
# -*- coding: utf-8  -*-

import requests
import os
import unicodedata
import re
import json

dbdir = os.path.abspath(os.path.join("..", "db"))
datadir = os.path.abspath(os.path.join("..", "data",))
if not os.path.exists(datadir):
	os.path.makedirs(datadir)
srcdir =  os.path.abspath(os.path.join("..", "src", "tanakh"))

def import_tanakh():

	mo = []
	oo = []
	oj = []
	jo = []
	to = []
	ta = []
	obj = json.load(open(os.path.join(dbdir, "books.json")))
	for book_number, (book_latin_name, book_name, chapters) in enumerate(obj, start=1):
		has_onkelos = book_number in [1, 2, 3, 4, 5]
		has_tafsir = book_number in [1, 2, 3, 4, 5]
		has_jerusalmi = book_number in [1, 2, 3, 4, 5]
		has_jonathan = book_number in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
		has_targum = book_number in [27, 28, 29, 30, 31, 32, 33, 34]

		f = os.path.join(srcdir, "tanakhus", "%02d.json"%book_number)
		mikra_lines = json.load(open(f))["text"]
		if book_number == 8:
			x = mikra_lines[23].pop(0)
			mikra_lines[22].append(x)
		mo.append(mikra_lines)

		if has_onkelos:
			f = os.path.join(srcdir, "onkelos", "%02d.json"%book_number)
			lines = json.load(open(f))["text"]
			oo.append(lines)
		else:
			oo.append([])

		if has_jerusalmi:
			f = os.path.join(srcdir, "jerusalmi", "%02d.json"%book_number)
			lines = json.load(open(f))["text"]
			for l in range(len(lines)):
				lines[l] += (len(mikra_lines[l]) - len(lines[l])) * [""]
			oj.append(lines)
		else:
			oj.append([])

		if has_jonathan:
			f = os.path.join(srcdir, "jonathan", "%02d.json"%book_number)
			lines = json.load(open(f))["text"]
			for l in range(len(lines)):
				lines[l] += (len(mikra_lines[l]) - len(lines[l])) * [""]
			jo.append(lines)
		else:
			jo.append([])

		if has_targum:
			f = os.path.join(srcdir, "targum", "%02d.json"%book_number)
			lines = json.load(open(f))["text"]
			for l in range(len(lines)):
				lines[l] += (len(mikra_lines[l]) - len(lines[l])) * [""]
			to.append(lines)
		else:
			to.append([])

		if has_tafsir:
			f = os.path.join(srcdir, "tafsir", "pentateuch.json")
			lines = list(json.load(open(f))["text"].values())[book_number]
			ta.append(lines)
		else:
			ta.append([])
		
	j = json.dumps(mo, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "mikra.json"), "w").write(j)
	j = json.dumps(oo, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "onkelos.json"), "w").write(j)
	j = json.dumps(oj, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "jerusalmi.json"), "w").write(j)
	j = json.dumps(jo, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "jonathan.json"), "w").write(j)
	j = json.dumps(to, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "targum.json"), "w").write(j)
	j = json.dumps(ta, ensure_ascii=False, indent="")
	open(os.path.join(datadir, "tafsir.json"), "w").write(j)


#		for chapter_number, num_verses in enumerate(chapters_obj, start=1):
#			for verse_number in range(1, num_verses + 1):
#				print (book_number, chapter_number, verse_number)



	exit()



#	con.commit()

	jsonfile = os.path.join(datadir, "parashot.json")
	pobj = json.load(open(jsonfile))
	vid = 1
	for parashah_number, (parashah_name, parashah_latin_name, book_number, num_verses, vobj) in enumerate(pobj, start=1):
		cur.execute("""INSERT INTO parashot(parashah_number, parashah_name, parashah_latin_name, book_number)
				VALUES(?, ?, ?, ?)""", (parashah_number, parashah_name, parashah_latin_name, book_number))
				#vobj[0], vobj[1], vobj[2], vobj[3], vobj[4], vobj[5], vobj[6]))
		for reading_number, num_verses in enumerate(vobj, start=1):
			for i in range(num_verses):
				cur.execute("""UPDATE verses SET parashah_number=?, reading_number=? WHERE rowid=?""",
						(parashah_number, reading_number, vid + i))
				#cur.execute("""INSERT INTO parashah_verses(parashah_number, reading_number, verse_rowid) VALUES(?, ?, ?)""",
				#		(parashah_number, reading_number, vid + i))
			vid += num_verses
	#con.commit()


	jsonfile = os.path.join(srcdir, "tafsir", "pentateuch.json")
	tafsir_dict = json.load(open(jsonfile))["text"]
	tafsir_lines = [tafsir_dict[name] for name in booknames[:5]]

	for book_number, (book_latin_name, book_name, chapters) in enumerate(obj, start=1):

		has_onkelos = book_number in [1, 2, 3, 4, 5]
		has_tafsir = book_number in [1, 2, 3, 4, 5]
		has_jerusalmi = book_number in [1, 2, 3, 4, 5]
		has_jonathan = book_number in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
		has_targum = book_number in [27, 28, 29, 30, 31, 32, 33, 34]

		jsonfile = os.path.join(srcdir, "rashi", "%02d.json"%book_number)
		rashi_lines = json.load(open(jsonfile))["text"]

		jsonfile = os.path.join(srcdir, "tanakhus", "%02d.json"%book_number)
		mikra_lines = json.load(open(jsonfile))["text"]
		if book_number == 8:
			x = mikra_lines[23].pop(0)
			mikra_lines[22].append(x)
		if has_onkelos:
			jsonfile = os.path.join(srcdir, "onkelos", "%02d.json"%book_number)
			onkelos_lines = json.load(open(jsonfile))["text"]
		if has_jerusalmi:
			jsonfile = os.path.join(srcdir, "jerusalmi", "%02d.json"%book_number)
			jerusalmi_lines = json.load(open(jsonfile))["text"]
		if has_jonathan:
			jsonfile = os.path.join(srcdir, "jonathan", "%02d.json"%book_number)
			jonathan_lines = json.load(open(jsonfile))["text"]
		if has_targum:
			jsonfile = os.path.join(srcdir, "targum", "%02d.json"%book_number)
			targum_lines = json.load(open(jsonfile))["text"]

		for chapter_number, num_verses in enumerate(chapters, start=1):
#			num_verses = len(mikra_lines[book_number - 1][chapter_number - 1]
			for verse_number in range(1, num_verses + 1):
				print (book_name, book_number, chapter_number, verse_number)
				mikra_text = mikra_lines[chapter_number - 1][verse_number - 1]
				rashi_text = rashi_lines[chapter_number - 1][verse_number - 1] if verse_number < len(rashi_lines[chapter_number - 1]) else ""
				cur.execute("""UPDATE verses SET
						mikra=?,
						rashi=?
						WHERE verse_number=? AND chapter_number=? AND book_number=?
						""", (mikra_text, "\n".join(rashi_text), verse_number, chapter_number, book_number))
				if has_onkelos:
					text = onkelos_lines[chapter_number - 1][verse_number - 1]
					# FIXES
					text = text.replace("\u200e", "").replace("???", "")
					text = re.sub("\(ס''א[^)]+\)", "", text)
					text = re.sub("\(נ''א[^)]+\)", "", text)
					text = re.sub("\(נ\u05f4א[^)]+\)", "", text)
					text = re.sub("\(נ'''*י[^)]+\)", "", text)
					text = re.sub("\(בכל הס':[^)]+\)", "", text)
					text = re.sub("\(לפרש״י[^)]+\)", "", text)
					text = re.sub("\(גי' רמב''ן [^)]+\)", "", text)
					text = re.sub("\: *ססס", "", text)
					#if text.endswith(":"):
					#	text = text[:-1]
					text = text.replace("  ", " ")
					fixes = (
							("א:ל", "א ל"),
							("ל:מִ", "ל מִ"),
							("ל:ל", "ל ל"),
							(":", ""),
							("[ ]+", " "),
							)
					for (src, dst) in fixes:
						text = re.sub(src, dst, text)
					text = text.strip()
						
					cur.execute("""UPDATE verses SET onkelos=? WHERE verse_number=? AND chapter_number=? AND book_number=?
							""", (text, verse_number, chapter_number, book_number))
				if has_jerusalmi:
					text = jerusalmi_lines[chapter_number - 1][verse_number - 1] if verse_number <= len(jerusalmi_lines[chapter_number - 1]) else ""
					# FIXES
					fixes = (("[:\n]", ''),
							('\(א"ה [^)]+\)', ''),
							('\(ס"א [^)]+\)', ''),
							('\(נ"א [^)]+\)', ''),
							('\(ונ"ל [^)]+\)', ''),
							('\[צ"ל [^]]+\]', ''),
							('צ"ל פרודיכון', ''),
							("¦", ""),
							("\(", " ("),
							("\)", ") "),
							("\[", " ["),
							("\]", "] "),
							("[\.\,]", ""), #punctuation
							("'", "׳"),
							("[ ]+", ' '))
					for (src, dst) in fixes:
						text = re.sub(src, dst, text)
					text = text.replace('"', '״').strip()
					cur.execute("""UPDATE verses SET jerusalmi=? WHERE verse_number=? AND chapter_number=? AND book_number=?
							""", (text, verse_number, chapter_number, book_number))
				if has_jonathan:
					text = jonathan_lines[chapter_number - 1][verse_number - 1] if verse_number <= len(jonathan_lines[chapter_number - 1]) else ""
					# FIXES
					fixes = (("[:\n]", ''),
							('\[ת"א\].+', ''),
							("\(", " ("),
							("\)", ") "),
							("\[", " ["),
							("\]", "] "),
							("[ ]+", " "))
					for (src, dst) in fixes:
						text = re.sub(src, dst, text)
					text = text.strip()
					cur.execute("""UPDATE verses SET jonathan=? WHERE verse_number=? AND chapter_number=? AND book_number=?
							""", (text, verse_number, chapter_number, book_number))
				if has_targum:
					text = targum_lines[chapter_number - 1][verse_number - 1]
					# FIXES
					fixes = ("[:\n]",
							"\<small\>תוספתא\<\/small\>",	#tosefta at Esther 1a
							"\<small\>",
							"\<\/small\>",
							'\[ת״\u200eא\]',	#broken t.a
							'\(בת"ק [^)]+\)',	#be.targumim.kdumim
							'\(בת"ק הגירסא [^)]+\)',
							'\(ג"ע [^)]+\)',	#gores a?
							'\(ס"א [^)]+\)',	#sfarim.aherim
							'\(ת"א[^)]*\)',	#targumim.aherim
							'\(ת"א[^)]+$',
							"\.",				# punctuation
							" ( )")
					for fix in fixes:
						text = re.sub(fix, "", text)
					text = text.strip()
					cur.execute("""UPDATE verses SET targum=? WHERE verse_number=? AND chapter_number=? AND book_number=?
							""", (text, verse_number, chapter_number, book_number))
				if has_tafsir:
					text = tafsir_lines[book_number - 1][chapter_number - 1][verse_number - 1]
					cur.execute("""UPDATE verses SET tafsir=? WHERE verse_number=? AND chapter_number=? AND book_number=?
							""", (text, verse_number, chapter_number, book_number))
		con.commit()


import_tanakh()
