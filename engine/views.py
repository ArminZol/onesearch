from django import forms
from django.http import Http404
from django.shortcuts import render
from .controllers import search
from onesearch.settings import BASE_DIR
from nltk.tokenize import word_tokenize 
from nltk.corpus import wordnet as wn
import json

class SearchForm(forms.Form):
	MODEL_CHOICES = [
		('boolean','Boolean Model'),
		('vsm','Vector Space Model')
	]
	query = forms.CharField(max_length=100, label='Search Query')
	model = forms.ChoiceField(choices=MODEL_CHOICES, widget=forms.RadioSelect, initial='boolean')

def index(request):
	form = SearchForm()
	courses_bigrams = {}
	reuters_bigrams = {}
	with open(BASE_DIR + '/processed/courses/word_bigrams.json') as file:
		courses_bigrams = json.load(file)
	with open(BASE_DIR + '/processed/reuters/word_bigrams.json') as file:
		reuters_bigrams = json.load(file)

	context = { 'form': form, 'courses_bigrams': courses_bigrams, 'reuters_bigrams': reuters_bigrams }
	return render(request, 'index.html', context)

def search_results(request):
	if request.method == 'GET':
		collection = request.GET['collection']
		processed_path = BASE_DIR + '/processed/' + collection
		query = request.GET['query']
		results = search(query, request.GET['model'], processed_path, collection, request.COOKIES.get('relevant'))
		documents = {}
		topics = {}
		with open(processed_path + '/preprocessed.json') as file:
			corpus = json.load(file)
			for doc in results[0]:
				if request.GET['model'] == 'boolean':
					documents[doc] = (corpus[doc], None)
				elif request.GET['model'] == 'vsm':
					documents[doc[0]] = (corpus[doc[0]], doc[1])

		# All code for wordnet from documentation: https://www.nltk.org/howto/wordnet.html
		expansion = {}
		for word in word_tokenize(query):
			synsets = wn.synsets(word)
			if synsets and len(synsets) < 5 and word not in expansion:
				expansion[word] = []
				for synset in wn.synsets(word):
					for hypernym in synset.hypernyms():
						for name in hypernym.lemma_names():
							if '_' not in name and name not in expansion[word]:
								expansion[word].append(name)
				if len(expansion[word]) == 0:
					del expansion[word]
	
		if collection == 'reuters':
			with open(processed_path + '/topics.json') as file:
				tmp = json.load(file)
				for doc in documents:
					topic = tmp[doc]
					if len(topic['topics']) == 0:
						if 'none' in topics:
							topics['none'].append(doc)
						else:
							topics['none'] = [doc]
					for t in topic['topics']:
						if t in topics:
							topics[t].append(doc)
						else:
							topics[t] = [doc]

		context = { 'collection': collection, 'query': query, 'documents':  documents, 'corrections': results[1], 'topics': topics, 'expansion': expansion }
		return render(request, 'results.html', context)
	raise Http404("No GET request")

def document(request, collection, doc_id):
	with open(BASE_DIR + '/processed/' + collection + '/preprocessed.json') as file:
		corpus = json.load(file)
		context = { 'doc_id': doc_id, 'document':  corpus[doc_id] }
		if collection == 'reuters':
			with open(BASE_DIR + '/processed/' + collection + '/topics.json') as topicsFile:
				context['topic'] = json.load(topicsFile)[doc_id]
		return render(request, 'document.html', context)
	return Http404("Missing Preprocessed File")