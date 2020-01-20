from django import forms
from django.http import Http404
from django.shortcuts import render

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
		tmp = SearchForm(request.GET)
		print(tmp)
	raise Http404("Poll does not exist") 