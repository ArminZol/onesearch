#!/usr/bin/env python

from bs4 import BeautifulSoup
from bs4.element import Tag
from utilities import BASE_DIR
import json
import os.path

# This code is designed directly from the Beautiful Soup documentation
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def parse_courses(processed_path):
	parsed = []
	count = 0
	for i in range(22):
		file_name = "reut2-0"
		if i < 10:
			file_name += "0"
		file_name += str(i) + ".sgm"
		print(file_name)
		with open(BASE_DIR + '/raw/reuters21578/' + file_name) as file:
			soup = BeautifulSoup(file, features='html.parser')
			docs = soup.find_all('text')
			for doc in docs:
				# Creates item with autogenerated document id
				item = {'id': count}
				for data in doc:
					if isinstance(data, Tag):
						if data.name == 'title':
							# Stores title
							item['title'] = data.string
						if data.name == 'body':
							item['body'] = data.string
				# If item is not empty (e.g. French, invalid format etc.)
				if 'title' in item and 'body' in item:
					parsed.append(item)
					count += 1

	# JSON write from https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file/20776329#20776329
	with open(processed_path, 'w') as outfile:
		json.dump(parsed, outfile, indent = 4, ensure_ascii = False)

# Throw error if file already generated
processed_path = BASE_DIR + "/processed/reuters/preprocessed.json"
if not os.path.isfile(processed_path):
	parse_courses(processed_path)
else:
	print('FILE ALREADY GENERATED')