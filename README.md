# Shopify Intern application
This project is for Shopify internship backend application

Requirements from: 
https://docs.google.com/document/d/1J49NAOIoWYOumaoQCKopPfudWI_jsQWVKlXmw1f1r-4/preview

The backend application is responsible for providing RESTful services of a barebone marketplace, which are written using [Python 3](https://www.python.org/) and [Flask](http://flask.pocoo.org/).

##Prerequisites: 
- Python 3.x.x environment

## To run the project(locally)

Mac OS:

### Install virtual environment
To avoid the mess of multiple versions, due to multiple local projects, it's recommended to take advantage of Python Virtual Enviromments, or simply [venv](https://docs.python.org/3/tutorial/venv.html).
in root folder:
```
python3 -m venv venv 
source venv/bin/activate
```
Windows:
```
py -3 -m venv venv
venv\Scripts\activate
```

### Install requirements 
```
pip install --upgrade pip
pip install -r requirements.txt
```
###initialize database
SQLite database is being used. A .sqlite file will be generated in the base dir.

Get into python env
```
python
```
Within python env, run these commands
```
>>> from server import db
>>> db.create_all()
```
### Running application
In a different terminal
```
python server.py
```

Swagger UI will be accessible at:

localhost:8000/gshop/api/v1/doc
