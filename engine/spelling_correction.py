from onesearch.settings import BASE_DIR
from scripts.utilities import is_stopword
import json

def correction(null_word):
	if len(null_word) < 4 or is_stopword(null_word):
		return None

	null_word = null_word.lower()

	possiblilities = []
	with open(BASE_DIR + '/raw_dictionary.json') as file:
		words = json.load(file)
		for word in words:
			if word[0] == null_word[0] and len(word) < len(null_word) + 3 and len(word) > len(null_word) - 3 and not is_stopword(word):
				possiblilities.append(word)

		if not possiblilities:
			return None

		candidate = {}
		for choice in possiblilities:
			edit_distance = weighted_distance(null_word, choice)
			if edit_distance < 5:
				candidate[choice] = words[choice]

		# Modified from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
		return [key for key,value in sorted(candidate.items(), key=lambda item: item[1], reverse=True)[:3]]


def is_vowel(c):
	return c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u' or c == 'y'

# Modified from https://stackoverflow.com/questions/2460177/edit-distance-in-python
def weighted_distance(s1, s2):
	if len(s1) > len(s2):
		s1, s2 = s2, s1

	distances = range(len(s1) + 1)
	for i2, c2 in enumerate(s2):
		distances_ = [i2+1]
		for i1, c1 in enumerate(s1):
			if c1 == c2:
				distances_.append(distances[i1])
			else:
				weight = 3

				# Swap vowel for vowel
				if is_vowel(c1) and is_vowel(c2):
					weight = 1
				# Swap or insert/delete consonent
				elif not is_vowel(c1) and not is_vowel(c2):
					weight = 2
				# Insert/delete vowel
				elif (not c1 or not c2) and (is_vowel(c1) or is_vowel(c2)):
					weight = 1

				distances_.append(weight + min((distances[i1], distances[i1 + 1], distances_[-1])))
		distances = distances_
	return distances[-1]

