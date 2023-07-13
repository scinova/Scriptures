#!/usr/bin/env python
# -*- coding: utf-8  -*-

import re

def strip_hebrew_accents(text):
	return re.sub('[\u0591-\u05ae]', '', text)

def strip_hebrew_points(text):
	return re.sub('[\u05b0-\u05bc\u05c7\u05c1\u05c2\u05bd]', '', text)

def strip_punctuation(text):
	text = re.sub('[\,\.\!\?\:\;\-—…]', '', text) #׳״
	return text

def strip_hebrew_punctuation(text):
	text = re.sub('[\u05c0\u05c3]', '', text)	#paseq and sofpasuk
	text = re.sub('[\u05be]', ' ', text)		#makaf
	return text

def strip_hebrew_double_points(text):
	return text.replace("\u05b0\u05b0", "\u05b0").replace("\u05bc\u05bc", "\u05bc")