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
	with open(BASE_DIR + '/raw/UofO_Courses.html') as file:
		soup = BeautifulSoup(file, features='html.parser')
		courses = soup.find_all('div', 'courseblock')
		count = 0
		for course in courses:
			# Creates item with autogenerated document id
			item = {'id': count}

			for data in course:
				if isinstance(data, Tag):
					if 'courseblocktitle' in data['class']:
						# French Validation
						if int(data.string[5]) >= 5:
							break
						# Stores title
						item['title'] = data.string
					if 'courseblockdesc' in data['class']:
						# Remove new line key from descriptions
						if data.string != None:
							item['body'] = data.string.replace('\n', '')
					if 'courseblockextra' in data['class']:
						break
			# If item is not empty (e.g. French, invalid format etc.)
			if 'title' in item:
				parsed.append(item)
				count += 1

	# JSON write from https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file/20776329#20776329
	with open(processed_path, 'w') as outfile:
		json.dump(parsed, outfile, indent = 2, ensure_ascii = False)

# Throw error if file already generated
processed_path = BASE_DIR + "/processed/courses/preprocessed.json"
if not os.path.isfile(processed_path):
	parse_courses(processed_path)
else:
	print('FILE ALREADY GENERATED')