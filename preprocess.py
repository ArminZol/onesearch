#!/usr/bin/env python

from bs4 import BeautifulSoup
from bs4.element import Tag
import json
import os.path

# This code is designed directly from the Beautiful Soup documentation
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def parse_courses():
	parsed = []
	with open('UofO_Courses.html') as file:
		soup = BeautifulSoup(file, features='html.parser')
		courses = soup.find_all('div', 'courseblock')
		for course in courses:
			item = {
				'doc_id': len(parsed)
			}
			for data in course:
				if isinstance(data, Tag):
					if 'courseblocktitle' in data['class']:
						if int(data.string[5]) >= 5:
							break
						item['title'] = data.string
					if 'courseblockdesc' in data['class']:
						# Remove new line key from descriptions
						if data.string != None:
							item['description'] = data.string.replace('\n', '')
					if 'courseblockextra' in data['class']:
						break
			if 'title' in item:
				parsed.append({
					'model': 'engine.document',
					'fields': item
				})

	# JSON write from https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file/20776329#20776329
	with open('preprocessed.json', 'w') as outfile:
		json.dump(parsed, outfile, indent = 4, ensure_ascii = False)

if not os.path.isfile('preprocessed.json'):
	parse_courses()
else:
	print('FILE ALREADY GENERATED')