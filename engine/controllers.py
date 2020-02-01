from engine.boolean import boolean_search
from engine.vsm import vsm_search
from onesearch.settings import BASE_DIR
import json

def search(query, model):
	with open(BASE_DIR + '/index.json') as indexFile:
		with open(BASE_DIR + '/settings.json') as settingsFile:
			index = json.load(indexFile)
			settings = json.load(settingsFile)
			if model == 'boolean':
				return boolean_search(query, index, settings)
			else:
				return vsm_search(query, index, settings)