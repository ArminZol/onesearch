#!/usr/bin/env python

from nltk.tokenize import word_tokenize 
from utilities import BASE_DIR, clean
import argparse
import json
import os
import math

if os.path.isfile(BASE_DIR + '/dictionary.json') or os.path.isfile(BASE_DIR + '/raw_dictionary.json') or os.path.isfile(BASE_DIR + '/index.json') or os.path.isfile(BASE_DIR + '/settings.json'):
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
# 	'word': {
#		'idf': 0
#		'documents': [
# 			{
#				'doc_id': 0,
#				'frequency': 1 
#				'tf-idf': 1
#			}
# 		]
#	}
# }
index = {}
dictionary = []
raw_dictionary = {}

with open(BASE_DIR + '/preprocessed.json') as file:
	data = json.load(file)
	for doc_id in data:
		doc = data[doc_id]
		words = word_tokenize(doc['title'])
		frequency = {}
		if 'description' in doc:
			words += word_tokenize(doc['description'])
		for word in words:
			if word.lower() in raw_dictionary:
				raw_dictionary[word.lower()] += 1
			else:
				raw_dictionary[word.lower()] = 1
				
			word = clean(word, settings)
			if word == None or word == '':
				continue
			if word in frequency:
				frequency[word] += 1
			else:
				frequency[word] = 1
		for word in frequency:
			if word not in index:
				index[word] = {}
				index[word]['documents'] = []
				dictionary.append(word)
			index[word]['documents'].append({
				'doc_id': doc_id,
				'frequency': frequency[word]
			})
	# Add VSM calculations to index
	num_docs = len(data)
	for word in index:
		index[word]['idf'] = math.log(num_docs / (len(index[word]['documents'])),10)
		for word_doc in index[word]['documents']:
			word_doc['tf-idf'] = word_doc['frequency'] * index[word]['idf']

with open(BASE_DIR + '/settings.json', 'w') as outfile:
	json.dump(settings, outfile, indent = 4, ensure_ascii = False)

with open(BASE_DIR + '/dictionary.json', 'w') as outfile:
	json.dump(dictionary, outfile, indent = 4, ensure_ascii = False)

with open(BASE_DIR + '/raw_dictionary.json', 'w') as outfile:
	json.dump(raw_dictionary, outfile, indent = 4, ensure_ascii = False)

with open(BASE_DIR + '/index.json', 'w') as outfile:
	json.dump(index, outfile, indent = 4, ensure_ascii = False)