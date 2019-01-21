# Shopify Intern application
This project is for Shopify internship backend application

Requirements from: 
https://docs.google.com/document/d/1J49NAOIoWYOumaoQCKopPfudWI_jsQWVKlXmw1f1r-4/preview

The backend application is responsible for providing RESTful services of a barebone marketplace, which are written using [Python 3](https://www.python.org/) and [Flask](http://flask.pocoo.org/).

App is at https://github.com/rzhangg/shopify

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

###APIs
Access the APIs through Swagger UI at localhost:8000/gshop/api/v1/doc

#### /item:
/item is basic url to access all item related queries

```
GET /item/{title}
```
Takes in title parameter
Will return item with queried title or return error message if not found

```
GET /item/all/{inventory_count}
```
Takes in inventory count
Will return all items found with inventory count more than queried value. To get all items pass in 0 as inventory_count
negative values will return error

```
POST /item/{title}&{price}&{inv_count}
```
Takes in 3 values; title, price, and inventory_count
creates new item in db with those values. Will return error if item already exists

```
PUT /item/buy/{title}{inv}
```
Purchase endpoint. pass in the title of the item you want to purchase and desired purchase quantity
Will try to purchase item, if successful will return new inventory_count for item
If you are trying to purchase more units then available, it will return error