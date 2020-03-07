from onesearch.settings import BASE_DIR
import json

# https://stackoverflow.com/questions/17821810/how-to-load-an-object-into-memory-for-entire-django-project-to-see

with open(BASE_DIR + '/processed/courses/index.json') as file:
	courses_index = json.load(file)

with open(BASE_DIR + '/processed/reuters/index.json') as file:
	reuters_index = json.load(file)
