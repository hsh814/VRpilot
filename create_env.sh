#!/bin/bash
## run this to create the virtual environment env
## you need to run /env/bin/activate to access env
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install --upgrade nltk
python3 -m pip install -r requirements.txt


