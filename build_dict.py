#!/usr/bin/env python

import argparse
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize 

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

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Build dictionary for search engine')
parser.add_argument('-wn', '--without-normalization', action='store_true', help='Use this flag to not normalize dictionary')
parser.add_argument('-ws', '--without-stemming', action='store_true', help='Use this flag to not stem dictionary')
parser.add_argument('-wsr', '--without-stopword-removal', action='store_true', help='Use this flag to keep stopwords in dictionary')
args = parser.parse_args()

dictionary = set()
with open('preprocessed.json') as file:
	data = json.load(file)
	for item in data:
		fields = item['fields']
		words = word_tokenize(fields['title'])
		if 'description' in fields:
			words += word_tokenize(fields['description'])
		for word in words:
			tmp = word
			if not args.without_stemming:
				tmp = stemmer(tmp)
			if not args.without_normalization:
				tmp = normalization(tmp)
			if not args.without_stopword_removal:
				if not is_stopword(tmp) and tmp.strip() != '':
					dictionary.add(tmp)
			elif tmp.strip() != '':
				dictionary.add(tmp)

dict_json = []
for word in dictionary:
	dict_json.append({
			'model': 'engine.word',
			'fields': {
				'word': word
			}
		})
with open('dictionary.json', 'w') as outfile:
	json.dump(dict_json, outfile, indent = 4, ensure_ascii = False)
