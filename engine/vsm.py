import json
from nltk.tokenize import word_tokenize 
from scripts.utilities import clean
from engine.spelling_correction import correction

def rocchio_query_expansion(query_vector, index, settings, collection, relevant_cookie):
	if relevant_cookie:
		relevance_dict = json.loads(relevant_cookie)
		relevant_vector = {}
		irrelevant_vector = {}
		count_relevant = 0
		count_irrelevant = 0
		if collection in relevance_dict:
			for query in relevance_dict[collection]:
				tokens = word_tokenize(query)
				for token in tokens:
					cleaned = clean(token, settings)
					if cleaned in index:
						for item in index[cleaned]['docs']:
							if str(item['id']) in relevance_dict[collection][query]:
								if relevance_dict[collection][query][str(item['id'])]:
									count_relevant += 1
									if cleaned in relevant_vector:
										relevant_vector[cleaned] += item['tf']
									else:
										relevant_vector[cleaned] = item['tf']
								else:
									count_irrelevant += 1
									if cleaned in irrelevant_vector:
										irrelevant_vector[cleaned] += item['tf']
									else:
										irrelevant_vector[cleaned] = item['tf']
		for word in relevant_vector:
			# Beta = 0.75
			value = 0.75 * (relevant_vector[word] / count_relevant)
			if word in query_vector:
				query_vector[word] += value
			else:
				query_vector[word] = value

		for word in irrelevant_vector:
			# Lambda = 0.15
			value = -0.15 * (irrelevant_vector[word] / count_irrelevant)
			if word in query_vector:
				query_vector[word] += value
			else:
				query_vector[word] = value
	return query_vector

def vsm_search(query, index, settings, processed_path, collection, relevant_cookie):
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

	query_vector = rocchio_query_expansion(query_vector, index, settings, collection, relevant_cookie)

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
	return ([(key,value) for key,value in sorted(docs_vector.items(), key=lambda item: item[1], reverse=True)[:15]], possible_corrections, query_vector)