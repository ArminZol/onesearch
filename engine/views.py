from django import forms
from django.http import Http404
from django.shortcuts import render
from .controllers import search
from onesearch.settings import BASE_DIR
from .index import courses_index, reuters_index
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
	context = { 'form': form }
	return render(request, 'index.html', context)

def search_results(request):
	if request.method == 'GET':
		collection = request.GET['collections']
		processed_path = BASE_DIR + '/processed/' + collection

		if collection == 'courses':
			results = search(request.GET['query'], request.GET['model'], processed_path, courses_index)
		elif collection == 'reuters':
			results = search(request.GET['query'], request.GET['model'], processed_path, reuters_index)

		documents = {}
		with open(processed_path + '/preprocessed.json') as file:
			corpus = json.load(file)
			for doc_id in results[0]:
				documents[doc_id] = corpus[doc_id]

		context = { 'collection': collection, 'documents':  documents, 'corrections': results[1] }
		return render(request, 'results.html', context)
	raise Http404("No GET request")

def document(request, collection, doc_id):
	with open(BASE_DIR + '/processed/' + collection + '/preprocessed.json') as file:
		corpus = json.load(file)
		context = { 'doc_id': doc_id, 'document':  corpus[doc_id] }
		return render(request, 'document.html', context)
	return Http404("Missing Preprocessed File")