#!/usr/bin/env python

import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def normalization(text):
	return text.replace('-', '').replace('.', '')

# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/
# Gets stems of words (auto decapitalizes as well)
ps = PorterStemmer() 
def stemmer(word):
	return ps.stem(word)

# https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
def is_stopword(word):
	return word in stopwords.words("english")

def clean(word, settings):
	if word == '':
		return None
	if settings['stemming']:
		word = stemmer(word)
	if settings['normalization']:
		word = normalization(word)
	if settings['stopword_removal'] and is_stopword(word):
		word = None
	return word