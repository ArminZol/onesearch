# OneSearch
Basic search engine built for CSI4107

It is not required to build this code as it is already running at https://one-search.herokuapp.com

# Setup
This setup incorporates Django and Virtual Environments to have web access

Prerequisites are that Python 3 and Pip are already installed on the machine.

 ```shell
# Create virtual environment
python3 -m venv env

# Activate environment
## On Mac
source env/bin/activate
## On Windows
env\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

python -m nltk.downloader stopwords punkt

# Run project - should be available at localhost:8000 on browser
python manage.py runserver
```

Each of the scripts that create json files for the project also need the virtual environment activated