from scripts.utilities import clean
from nltk.tokenize import word_tokenize 
from django.http import UnreadablePostError
from onesearch.settings import BASE_DIR
import json

def is_operator(token):
	return token == 'AND' or token == 'OR' or token == 'AND_NOT'

def peek(stack):
    return stack[-1] if stack else None

# Modified from https://en.wikipedia.org/wiki/Shunting-yard_algorithm
# http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html
def postfix_to_infix(query):
	tokens = word_tokenize(query)
	operatorStack = []
	outputQueue = []

	for token in tokens:
		if token == '(':
			operatorStack.append('(')
		elif token == ')':
			top = peek(operatorStack)
			while top is not None and top != '(':
				outputQueue.append(operatorStack.pop())
				if not operatorStack:
					raise UnreadablePostError('Unbalanced parentheses')
				top = peek(operatorStack)
			operatorStack.pop()
		elif is_operator(token):
			top = peek(operatorStack)
			while top is not None and top not in '()':
				outputQueue.append(operatorStack.pop())
				top = peek(operatorStack)
			operatorStack.append(token)
		else: # Word
			outputQueue.append(token)

	while operatorStack:
		outputQueue.append(operatorStack.pop())
	
	return outputQueue

## Copy of way it was done in lecture notes
def boolean_calculate(ids1, ids2, operator):
	answer = []
	if operator == 'AND':
		p1 = 0
		p2 = 0
		while p1 < len(ids1) and p2 < len(ids2):
			if ids1[p1] == ids2[p2]:
				answer.append(ids1[p1])
				p1 += 1
				p2 += 1
			elif ids1[p1] < ids2[p2]:
				p1 += 1
			else:
				p2 += 1
	elif operator == 'OR':
		p1 = 0
		p2 = 0
		while p1 < len(ids1) and p2 < len(ids2):
			if ids1[p1] == ids2[p2]:
				answer.append(ids1[p1])
				p1 += 1
				p2 += 1
			elif ids1[p1] < ids2[p2]:
				answer.append(ids1[p1])
				p1 += 1
			else:
				answer.append(ids2[p2])
				p2 += 1

		while p1 < len(ids1):
			answer.append(ids1[p1])
			p1 += 1
		while p2 < len(ids2):
			answer.append(ids2[p2])
			p2 += 1
	else: # AND_NOT
		p1 = 0
		p2 = 0
		while p1 < len(ids1) and p2 < len(ids2):
			if ids1[p1] == ids2[p2]:
				p1 += 1
				p2 += 1
			elif ids1[p1] < ids2[p2]:
				p1 += 1
			else:
				answer.append(ids2[p2])
				p2 += 1
		while p2 < len(ids2):
			answer.append(ids2[p2])
			p2 += 1
	return answer

def word_to_ids(word_list):
	ids = []
	for item in word_list:
		ids.append(item['doc_id'])
	return ids

def handle_wildcard(word, index):
	split = word.split('*')
	word_bigram = []
	for part in split:
		if part != '':
			# If there exists content before the * then add $
			if part == split[0]:
				word_bigram.append('$' + part[0])
			elif part == split[-1]:
				word_bigram.append(part[-1] + '$')
			
			for i in range(0, len(part)-1):
				word_bigram.append(part[i:i+2])

	if len(word_bigram) == 0:
		return []

	with open(BASE_DIR + '/bigrams.json') as file:
		bigrams = json.load(file)
		words = sorted(bigrams[word_bigram[0]])
		for i in range(1, len(word_bigram)):
			words = boolean_calculate(words, sorted(bigrams[word_bigram[i]]), 'AND')

		if len(words) == 0:
			return []

		documents = []
		for word in words:
			documents = boolean_calculate(documents, word_to_ids(index[word]['documents']), 'OR')
		return documents

def boolean_search(query, index, settings):
	infix = postfix_to_infix(query)
	stack = []
	for item in infix:
		if is_operator(item):
			ids1 = stack.pop()
			ids2 = stack.pop()
			stack.append(boolean_calculate(ids1, ids2, item))
		else:
			ids = []
			cleaned = clean(item, settings)
			if '*' in cleaned:
				ids = handle_wildcard(cleaned, index)
			elif cleaned and cleaned in index:
				ids = word_to_ids(index[cleaned]['documents'])
			stack.append(ids)
	return stack.pop()
