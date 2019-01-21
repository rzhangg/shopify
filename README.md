# shopify
shopify challenge for backend 

Requirements: 
https://docs.google.com/document/d/1J49NAOIoWYOumaoQCKopPfudWI_jsQWVKlXmw1f1r-4/preview

Prerequisites: Python 3.6 environment

Linux:

1. Install virtual environment using

in root folder:

python3 -m venv venv 

2. to activate virtual environment

source venv/bin/activate

3. install requirements 

pip install -r requirements.txt

4. initialize database

python
>>> from server import db

>>> db.create_all()

Database has been initialized you should see crud.sqlite
5. In different terminal
python server.py

To run
localhost:8000/api/v1/doc
