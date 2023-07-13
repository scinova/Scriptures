from flask import Flask, g
from flask import render_template, send_from_directory, request, redirect

import difflib
import unicodedata
import utils

import Scriptures
scriptures = Scriptures.Scriptures()
import Aramaic
aramaic = Aramaic.Aramaic()

def create_app():
	app = Flask(__name__, template_folder="html")
	app.jinja_env.globals['lstrip_blocks'] = True
	app.jinja_env.globals['trim_blocks'] = True

	@app.context_processor
	def inject_variables():
		return dict(
				type=type, dir=dir, len=len, int=int, ord=ord, chr=chr, list=list, str=str, set=set, sorted=sorted, hex=hex, hasattr=hasattr,
				difflib=difflib,enumerate=enumerate, unicodedata=unicodedata,
				scriptures=scriptures,
				aramaic=aramaic,
				Aramaic=Aramaic,
				strip_hebrew_points=utils.strip_hebrew_points
		)

	@app.route('/@@/<path:filename>')
	def files(filename):
		return send_from_directory('static', filename)

	@app.route('/@@/fonts/<path:filename>')
	def fonts(filename):
		return send_from_directory('../fonts', filename)

	@app.route('/aramaic')
	def aramaic_main():
		return render_template('aramaic.html')

	@app.route('/aramaic/verbs')
	def aramaic_verbs():
		return render_template('aramaic-verbs.html')

	@app.route('/aramaic/nouns')
	def aramaic_nouns():
		return render_template('aramaic-nouns.html')

	@app.route('/aramaic/numbers')
	def aramaic_numbers():
		return render_template('aramaic-numbers.html')

	@app.route('/aramaic/<string:bareword>')
	def aramaic_word(bareword):
		return render_template('aramaic-word.html', bareword=bareword)

	@app.route('/dev')
	def dev():
		return render_template('dev.html')

	@app.route('/')
	def main():
		return render_template('index.html')

	@app.route('/tanakh')
	def tanakh_main():
		return render_template('tanakh.html')

	@app.route('/talmud')
	def talmud_main():
		return render_template('talmud.html')

	@app.route('/talmud/<int:tractate_number>')
	def tractate(tractate_number):
		tractate = scriptures.talmud.tractates[tractate_number - 1]
		return render_template('talmud-tractate.html', tractate=tractate)

	@app.route('/talmud/<int:tractate_number>/<int:folio><string:side>')
	def page(tractate_number, folio, side):
		side = 0 if side == 'a' else 1
		pageidx = (folio - 2) * 2 + side
		page = scriptures.talmud.tractates[tractate_number - 1].pages[pageidx]
		return render_template('talmud-page.html', page=page)

	@app.route('/talmud/<int:order_number>/<int:tractate_number>/articles/<int:article_number>')
	def article(order_number, tractate_number, article_number):
		article = db.talmud.orders[order_number - 1].tractates[tractate_number - 1].articles[article_number - 1]
		return render_template('talmud-article.html', article=article)

	@app.route('/talmud/<int:order_number>/<int:tractate_number>/<int:chapter_number>')
	def chapter(order_number, tractate_number, chapter_number):
		chapter = db.talmud.orders[order_number - 1].tractates[tractate_number - 1].chapters[chapter_number - 1]
		return render_template('talmud-chapter.html', chapter=chapter)

	@app.route('/talmud/<int:order_number>/<int:tractate_number>/<int:chapter_number>/<int:section_number>')
	def section(order_number, tractate_number, chapter_number, section_number):
		section = db.talmud.orders[order_number - 1].tractates[tractate_number - 1].chapters[chapter_number - 1].sections[section_number - 1]
		return render_template('talmud-section.html', section=section)

	@app.route('/zohar')
	def zohar_main():
		return render_template('zohar.html')

	@app.route('/words')
	def words():
		return render_template('words.html')

	@app.route('/zohar/<int:chapter_number>')
	def zohar_chapter(chapter_number):
		chapter = scriptures.zohar.chapters[chapter_number - 1]
		return render_template('zohar-chapter.html', chapter=chapter)

	@app.route('/zohar/<int:chapter_number>/<int:article_number>')
	def zohar_article(chapter_number, article_number):
		chapter = scriptures.zohar.chapters[chapter_number - 1]
		article = chapter.articles[article_number - 1]
		return render_template('zohar-article.html', article=article)

	@app.route('/tanakh/<int:book_number>/<int:chapter_number>')
	def view_tanakh_chapter(book_number, chapter_number):
		book = scriptures.tanakh.books[book_number - 1]
		chapter = book.chapters[chapter_number - 1]
		return render_template('tanakh-chapter.html', chapter=chapter)

	@app.route('/tanakh/p/<int:parashah_number>')
	def view_tanakh_parashah(parashah_number):
		parashah = scriptures.tanakh.parashot[parashah_number - 1]
		return render_template('tanakh-parashah.html', parashah=parashah)
	return app
