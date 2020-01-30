#!/usr/bin/env python

from nltk.tokenize import word_tokenize 
from utilities import BASE_DIR, clean
import argparse
import json
import os

if os.path.isfile(BASE_DIR + '/dictionary.json') or os.path.isfile(BASE_DIR + '/index.json') or os.path.isfile(BASE_DIR + '/settings.json'):
	raise Exception("dictionary/index/settings already exists")


# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Build dictionary for search engine')
parser.add_argument('-wn', '--without-normalization', action='store_true', help='Use this flag to not normalize dictionary')
parser.add_argument('-ws', '--without-stemming', action='store_true', help='Use this flag to not stem dictionary')
parser.add_argument('-wsr', '--without-stopword-removal', action='store_true', help='Use this flag to keep stopwords in dictionary')
args = parser.parse_args()

settings = {}

if args.without_stemming:
	settings['stemming'] = False
else:
	settings['stemming'] = True
if args.without_normalization:
	settings['normalization'] = False
else:
	settings['normalization'] = True
if args.without_stopword_removal:
	settings['stopword_removal'] = False
else:
	settings['stopword_removal'] = True

# index = {
# 	'word': [
# 		{
#			'doc_id': 0,
#			'frequency': 1 
#		}
# 	]
# }
index = {}
dictionary = []

with open(BASE_DIR + '/preprocessed.json') as file:
	data = json.load(file)
	for item in data:
		doc_id = item['fields']['doc_id']
		words = word_tokenize(item['fields']['title'])
		frequency = {}
		if 'description' in item['fields']:
			words += word_tokenize(item['fields']['description'])
		for word in words:
			word = clean(word, settings)
			if word == None:
				continue
			if word in frequency:
				frequency[word] += 1
			else:
				frequency[word] = 1
		for word in frequency:
			if word not in index:
				index[word] = []
				dictionary.append(word)
			index[word].append({
				'doc_id': doc_id,
				'frequency': frequency[word]
			})

with open(BASE_DIR + '/settings.json', 'w') as outfile:
	json.dump(settings, outfile, indent = 4, ensure_ascii = False)

with open(BASE_DIR + '/dictionary.json', 'w') as outfile:
	json.dump(dictionary, outfile, indent = 4, ensure_ascii = False)

with open(BASE_DIR + '/index.json', 'w') as outfile:
	json.dump(index, outfile, indent = 4, ensure_ascii = False)