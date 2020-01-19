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

# Setup and run project - should be available at localhost:8000
python manage.py migrate
python manage.py runserver
```

# Pre-Processing (Module 2)
Currently, this project uses an independant python script `preprocess.py` in the root directory to filter core data from the uOttawa Courses page (UofO_courses.html in root directory) and store the cleaned version in preprocessed.json in a json format. This requires for the html file to be present in the root directory, and will not run if the generated preprocessed.json file is already made.

This does this using BeautifulSoup to parse through the html code, find each individual course in a div tag with class "courseblock", then grabs the title from class "courseblocktitle", and description from "courseblockdesc".

This script can be run by activating the virtual environment with all the dependencies install and running `python preprocess.py`

The JSON file created is formatted so that Django can ingest the data directly into its db with `python manage.py loaddata preprocessed.json`

# Building the Dictionary (Module 3)