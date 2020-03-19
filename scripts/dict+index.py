#!/usr/bin/env python

from nltk.tokenize import word_tokenize 
from utilities import BASE_DIR, clean
import argparse
import json
import math
import progressbar

# index = {
# 	'word': {
#		'idf': 0
#		'docs': [
# 			{
#				'id': 0,
#				'tf': 1 
#			}
# 		]
#	}
# }
def save_dict_index(path):
	index = {}
	dictionary = []
	raw_dictionary = {}

	with open(path + '/preprocessed.json') as file:
		data = json.load(file)
		# https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
		bar = progressbar.ProgressBar(maxval=len(data))
		bar.start()
		for doc in data:
			words = word_tokenize(doc['title'])
			frequency = {}
			if 'body' in doc:
				words += word_tokenize(doc['body'])
			for word in words:
				word = word.lower()
				if word in raw_dictionary:
					raw_dictionary[word] += 1
				else:
					raw_dictionary[word] = 1
					
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
					index[word]['docs'] = []
					dictionary.append(word)
				index[word]['docs'].append({
					'id': doc['id'],
					'tf': frequency[word]
				})
			bar.update(doc['id'])
		bar.finish()
		# Add VSM calculations to index
		num_docs = len(data)
		for word in index:
			index[word]['idf'] = math.log(num_docs / (len(index[word]['docs'])),10)

	with open(path + '/dictionary.json', 'w') as outfile:
		json.dump(dictionary, outfile, indent = 2, ensure_ascii = False)

	with open(path + '/raw_dictionary.json', 'w') as outfile:
		json.dump(raw_dictionary, outfile, indent = 2, ensure_ascii = False)

	with open(path + '/index.json', 'w') as outfile:
		json.dump(index, outfile, ensure_ascii = False)



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

with open(BASE_DIR + '/processed/settings.json', 'w') as outfile:
	json.dump(settings, outfile, indent = 2, ensure_ascii = False)

print("Starting Courses...")
save_dict_index(BASE_DIR + "/processed/courses")

print("Starting Reuters...")
save_dict_index(BASE_DIR + "/processed/reuters")
