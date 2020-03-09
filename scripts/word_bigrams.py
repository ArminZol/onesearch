#!/usr/bin/env python

from nltk.tokenize import word_tokenize 
from utilities import BASE_DIR
import json
import progressbar

def save_bigrams(path):
	bigrams = {}

	with open(path + '/preprocessed.json') as textFile:
		with open(path + '/raw_dictionary.json') as dictFile:
			docs = json.load(textFile)
			dictionary = json.load(dictFile)

			# https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
			bar = progressbar.ProgressBar(maxval=len(docs))
			bar.start()

			for doc in docs:
				words = word_tokenize(doc['title'])
				if 'body' in doc:
					words += word_tokenize(doc['body'])
				for i in range(1, len(words)):
					word1 = words[i-1].lower()
					word2 = words[i].lower()
					if len(word1) > 1 and len(word2) > 1:
						increment = 1 / dictionary[word1]
						if word1 in bigrams:
							if word2 in bigrams[word1]:
								bigrams[word1][word2] += increment
							else:
								bigrams[word1][word2] = increment
						else:
							bigrams[word1] = { word2: increment }
				bar.update(doc['id'])
			bar.finish()

	with open(path + '/word_bigrams.json', 'w') as outfile:
		json.dump(bigrams, outfile, indent = 2, ensure_ascii = False)

print("Starting Courses...")
save_bigrams(BASE_DIR + "/processed/courses")

print("Starting Reuters...")
save_bigrams(BASE_DIR + "/processed/reuters")
