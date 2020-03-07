from nltk.tokenize import word_tokenize 
from scripts.utilities import clean
from engine.spelling_correction import correction

def vsm_search(query, index, settings, tmp_correction):
	tokens = word_tokenize(query)
	query_vector = {}
	possible_corrections = {}

	for token in tokens:
		tmp = clean(token, settings)
		if tmp not in index:
			tmp_correction = correction(token, processed_path)
			if tmp_correction:
				possible_corrections[token] = tmp_correction
		if tmp in query_vector:
			query_vector[tmp] += 1
		else:
			query_vector[tmp] = 1

	docs_vector = {}
	for word in query_vector:
		if word in index:
			for doc in index[word]['docs']:
				value = query_vector[word] * doc['tf'] * index[word]['idf']
				if doc['id'] in docs_vector:
					docs_vector[doc['id']] += value
				else:
					docs_vector[doc['id']] = value

	# Modified from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
	# print({k: v for k, v in sorted(docs_vector.items(), key=lambda item: item[1], reverse=True)}) # Left here for debugging
	return ([(key,value) for key,value in sorted(docs_vector.items(), key=lambda item: item[1], reverse=True)[:15]], possible_corrections)