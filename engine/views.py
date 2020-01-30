from django import forms
from django.http import Http404
from django.shortcuts import render
from .controllers import boolean_search
from .models import Document

class SearchForm(forms.Form):
	query = forms.CharField(max_length=100, label='Search Query')

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
		
		# tmp = SearchForm(request.GET)
		# for item in request.GET['query']:
		results = boolean_search(request.GET['query'])
		tmp = Document.objects.filter(doc_id__in=results)
		context = { 'results':  tmp }
		return render(request, 'results.html', context)
	raise Http404("Poll does not exist")

def document(request, id):
	tmp = Document.objects.get(doc_id=id)
	print(tmp)
	context = { 'document':  tmp }
	return render(request, 'document.html', context)