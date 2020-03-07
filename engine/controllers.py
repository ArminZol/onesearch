from engine.boolean import boolean_search
from engine.vsm import vsm_search
from onesearch.settings import BASE_DIR
import json

def search(query, model, processed_path, index):
	with open(BASE_DIR + '/processed/settings.json') as settingsFile:
		settings = json.load(settingsFile)
		if model == 'boolean':
			return boolean_search(query, index, settings, processed_path)
		else:
			return vsm_search(query, index, settings, processed_path)