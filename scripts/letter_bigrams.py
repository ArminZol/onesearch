#!/usr/bin/env python

from utilities import BASE_DIR
import json

def save_letter_bigrams(path):
	with open(path + '/dictionary.json') as file:
		data = json.load(file)
		# {
		#	'$a': [ alternate ]
		# }
		bigrams = {}
		for word in data:
			if word == None or word == '':
				continue

			word_bigram = set()
			word_bigram.add('$' + word[0])
			if len(word) > 1:
				word_bigram.add(word[-1] + '$')
			for i in range(0, len(word)-1):
				word_bigram.add(word[i:i+2])

			for item in word_bigram:
				if item in bigrams:
					bigrams[item].append(word)
				else:
					bigrams[item] = [word]

	with open(path + '/letter_bigrams.json', 'w') as outfile:
		json.dump(bigrams, outfile, indent = 4, ensure_ascii = False)

print("Starting Courses...")
save_letter_bigrams(BASE_DIR + "/processed/courses")

print("Starting Reuters...")
save_letter_bigrams(BASE_DIR + "/processed/reuters")
