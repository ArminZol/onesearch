from django import forms
from django.http import Http404
from django.shortcuts import render
from .controllers import search
from onesearch.settings import BASE_DIR
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
	# if request.method == 'POST':
	# 	tmp = SearchForm(request.POST)
	# 	print(tmp)
	# 	data = 'TEST'
	context = { 'form': form }
	return render(request, 'index.html', context)

def search_results(request):
	if request.method == 'GET':
		results = search(request.GET['query'], request.GET['model'])
		documents = {}
		with open(BASE_DIR + '/preprocessed.json') as file:
			corpus = json.load(file)
			for doc_id in results:
				documents[doc_id] = corpus[doc_id]

		context = { 'documents':  documents }
		return render(request, 'results.html', context)
	raise Http404("No GET request")

def document(request, doc_id):
	with open(BASE_DIR + '/preprocessed.json') as file:
		corpus = json.load(file)
		context = { 'doc_id': doc_id, 'document':  corpus[doc_id] }
		return render(request, 'document.html', context)
	return Http404("Missing Preprocessed File")