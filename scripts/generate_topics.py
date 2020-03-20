from utilities import BASE_DIR, clean
from nltk.tokenize import word_tokenize 
import json
import progressbar

path = BASE_DIR + "/processed"

topics = []

with open(path + '/reuters/topics.json') as file:
	topics = data = json.load(file)

with open(path + '/reuters/preprocessed.json') as preprocessedFile, \
		open(path + '/reuters/index.json') as indexFile, \
		open(path + '/settings.json') as settingsFile:
	preprocessed = json.load(preprocessedFile)
	index = json.load(indexFile)
	settings = json.load(settingsFile)

	bar = progressbar.ProgressBar(maxval=len(topics))
	bar.start()

	for topic in topics:
		if topic['assigned'] == False:
			scores = {}
			word_count = {}
			doc = preprocessed[topic['id']]
			words = word_tokenize(doc['title'])
			if 'body' in doc:
				words += word_tokenize(doc['body'])
			for word in words:
				tmp_word = clean(word.lower(), settings)
				if tmp_word == None or tmp_word == '':
					continue
				if tmp_word in word_count:
					word_count[tmp_word] += 1
				else:
					word_count[tmp_word] = 1
			for word in word_count:
				for item in index[word]['docs']:
					if item['id'] != topic['id'] and 'topics' in topics[item['id']]: # Only find score of objects that have topics
						if item['id'] in scores:
							scores[item['id']] += item['tf'] * index[word]['idf'] * word_count[word]
						else:
							scores[item['id']] = item['tf'] * word_count[word]
			nn = [key for key,value in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]]
			new_topics = []
			if len(nn) > 1:
				topics1 = set(topics[nn[0]]['topics'])
				topics2 = set(topics[nn[1]]['topics'])
				topics3 = {}
				if len(nn) > 2:
					topics3 = set(topics[nn[2]]['topics'])
				new_topics = list((topics1 & topics2) | (topics1 & topics3) | (topics2 & topics3))
			topic['topics'] = new_topics
		bar.update(topic['id'])
	bar.finish()

with open(path + '/reuters/topics.json', 'w') as outfile:
	json.dump(topics, outfile, indent = 2, ensure_ascii = False)
