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