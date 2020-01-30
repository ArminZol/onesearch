# OneSearch
Basic search engine built for CSI4107

# Setup
This setup incorporates Django and Virtual Environments to have web access

Prerequisites are that Python 3 is already installed on the machine.

 ```shell
# Create virtual environment
python3 -m venv env

# Activate environment
## On Mac
source env/bin/activate
## On Windows
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run project - should be available at localhost:8000
python manage.py runserver
```

# Pre-Processing (Module 2)
This project uses an independant python script `preprocess.py` in the **scripts directory** to filter the uOttawa Courses page (UofO_courses.html) and store it in `preprocessed.json` in the root directory. This requires for the html file to be present, and will not run if the generated preprocessed.json file is already made.

This does this using BeautifulSoup to parse through the html code, splits individual course by identifying div tags with class "courseblock", then grabs the title from class "courseblocktitle", and description from "courseblockdesc".

```html
<div class="courseblock">
	<p class="courseblocktitle noindent"><strong>PSY 7190 Seminars in Psychology II (3 units)</strong></p>
	<p class="courseblockdesc noindent">Selected topics on contemporary psychology presented and discussed as graduate seminars.</p>
	<p class="courseblockextra noindent"><strong>Course Component: </strong>Lecture</p>
</div>
```

It will then store its title, description, and autogenerate a document id based on the order it is found in.

This automatically filters french courses by ignoring any classes where the second digit of the course number is greater than or equal to 5 (e.g. ADM 2703 is a french course as indicated by the 7)
> There are a few courses that are bilingual and therefore still included in the preprocessed data (e.g. PSY 5023, PSY 6002 etc.)

This script can be run by activating the virtual environment with all the dependencies installed and running `python scripts/preprocess.py`

The JSON file created is formatted so that Django can ingest the data directly into its db.

```json
{
	"model": "engine.document",
	"fields": {
		"doc_id": 347,
		"title": "PSY 7190 Seminars in Psychology II (3 units)",
		"description": "Selected topics on contemporary psychology presented and discussed as graduate seminars."
	}
}
```
> engine.document simply indicates that it will inserted into the database as a document

# Building the Dictionary and Index (Module 3 and 4)
These modules were joined into one script `process/build_dict.py` as both the dictionary and index already required going through `preprocessed.json`

The script takes arguments for not using stemming, normalization and stopword removal (`python process/build_dict.py --help` to see the arguments) but these are all enabled by default as required. Similarly this can be run using the same manner by activating the virtual environment and running `python process/build_dict.py`, and again will generate the files in the root directory.
> Case folding is already done by default with the NLTK stemming module
> One interesting observation is that the NLTK tokenization stores commas as an individual word

It will output 3 different files:

First is the dictionary file `dictionary.json`, which stores all the words in a list within json that is easily readable by python.
```json
[
	"adm"
    
]
```

Next is `index.json` which is a simple json file with the inverted index. It stores which documents each word is located as well as its frequency (the amount of times occured in the document)
```json
"adm": [
	{
		"doc_id": 0,
		"frequency": 1
	}
]
```

It will also store `settings.json` which stores the settings used to create the Dictionary so the engine can clean the query in the same way

# Corpus Access (Module 5)
By creating the `preprocessed.json` file in that format, it can be ingested by Django, and will then have native access Django's MySQL database for simple native access.

> Note: The database has already been created and saved so there is no need from this (`db.sqlite3`). A visual representation of the data available in the DB is available at `localhost:8000/admin` which login *admin* and password *admin*. If this is going to be done again `db.sqlite3` must be deleted first.

This data was ingested using
```shell
python manage.py migrate
python manage.py loaddata preprocessed.json
```

An example of the retrival would then be `Document.objects.filter(doc_id__in=list_of_ids)` which will return all the Documents from the list in a dictionary style format called a QuerySet.