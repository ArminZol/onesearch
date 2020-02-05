# OneSearch
Basic search engine built for CSI4107

It is not required to build this code as it is already running at https://one-search.herokuapp.com

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

python -m nltk.downloader stopwords punkt

# Run project - should be available at localhost:8000 on browser
python manage.py runserver
```

# User Interface (Module 1)
This project leverages Django's framework to create a simple user interface using html. These views are all controlled through `engine/view.py` with their respective HTML templates being located in the templates folder. 

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

The JSON file is created and an ID is generated based on its collection and the order it appeared in

```json
{
	"UO_347": {
		"title": "PSY 7190 Seminars in Psychology II (3 units)",
		"description": "Selected topics on contemporary psychology presented and discussed as graduate seminars."
	}
}
```

# Building the Dictionary and Index (Module 3 and 4 and 8a (VSM Weight Calculation))
These modules were joined into one script `process/dict+index.py` as both the dictionary and index already required going through `preprocessed.json`

The script takes arguments for not using stemming, normalization and stopword removal (`python process/build_dict.py --help` to see the arguments) but these are all enabled by default as required. Similarly this can be run using the same manner by activating the virtual environment and running `python process/build_dict.py`, and again will generate the files in the root directory.
> Case folding is already done by default with the NLTK stemming module
> One interesting observation is that the NLTK tokenization stores commas, brackets etc.. as an individual words which may have adverse results

It will output 4 different files:

First is the dictionary file `dictionary.json`, which stores all the words in a list within json that is easily readable by python.
```json
[
	"adm"
]
```

Next is `index.json` which is a simple json file with the inverted index. It stores which documents each word is located as well as its frequency, tf-idf, and idf
```json
"adm": {
	"documents": [
		{
			"doc_id": "UO_0",
			"frequency": 1,
			"tf-idf": 0.49633151327271724
		}
	],
	"idf": 0.49633151327271724
}
```

It will also store `settings.json` which stores the settings used to create the Dictionary so the engine can clean the query in the same way and `raw_dictionary.json` which stores all words and their frequency without any cleaning except case folding (for spelling correction module)

# Corpus Access (Module 5)
Data gets accessed directly from the index to be displayed in the `search_results` function within `engine/views.py`. It will display every document title, and its description up to 100 characters. The title is also selectable to go to the full document. Since the json will be ingested by Python as a dictionary, the document retreival should be on average in constant time (O(1)).

# Boolean Retreival Model (Module 6)
The boolean model is available within `engine/boolean.py`, and it processes the query by changing the string to an postfix stack, then processing each word individually by converting it to its list of documents.

# Wildcard Management (Module 7)
Also located within `engine/boolean.py`, the `handle_wildcard` function splits a word into its elements, then uses their bigrams to find common documents. 

The function also cleans the word regardless of it containing a wildcard, so if stemming is on, the word with a wildcard will also be stemmed.

An indipendant script `scripts/bigrams.py` is used to generate a `bigrams.json` file with all the bigrams and their relationship to words in the dictionary. If the bigram is one letter it will appear as $a

# Vector Space Model (Module 8)
As mentioned prior, the calculations for tf, idf, and tf-idf were already done and stored in the index. The retreival model would be located in `engine/vsm.py`, where the top 15 documents are found and returned.

# Spelling Correction with Weighted Edit Distance (Module 9)
This is located in `engine/spelling_correction.py`. Any words that had no corresponding documents would be passed into the function `correction` to be evaluated. If it is a stopword or less than 4 characters it would be ignored.

When searching for words to evaluate weighted edit distance, it only considers words in the raw dictionary that has a length of +/- 3 characters. It then calculates weighted edit distances, and only keeps words with a distance of less than 5, then sorts those words by raw frequency.

When calculating weighted edit distance, I thought of this [article](https://www.dailywritingtips.com/7-types-of-misspellings/) and put less weight on insertion and replacement of vowels (weight of 1), a weight of 2 for substitution of consonants, and a weight of 3 for everything else (insertion/deletion of consonants...)
