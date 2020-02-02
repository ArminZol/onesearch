from nltk.tokenize import word_tokenize 
from scripts.utilities import clean
from engine.spelling_correction import correction

def vsm_search(query, index, settings):
	tokens = word_tokenize(query)
	query_vector = {}
	possible_corrections = {}

	for token in tokens:
		tmp = clean(token, settings)
		if tmp not in index:
			tmp_correction = correction(token)
			if tmp_correction:
				possible_corrections[token] = correction(token)
		if tmp in query_vector:
			query_vector[tmp] += 1
		else:
			query_vector[tmp] = 1

	docs_vector = {}
	for word in query_vector:
		if word in index:
			for doc in index[word]['documents']:
				value = query_vector[word] * doc['tf-idf']
				if doc['doc_id'] in docs_vector:
					docs_vector[doc['doc_id']] += value
				else:
					docs_vector[doc['doc_id']] = value

	# Modified from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
	# print({k: v for k, v in sorted(docs_vector.items(), key=lambda item: item[1], reverse=True)}) # Left here for debugging
	return ([key for key,value in sorted(docs_vector.items(), key=lambda item: item[1], reverse=True)[:15]], possible_corrections)