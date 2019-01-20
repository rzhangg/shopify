import os
import logging

from flask import Flask, g, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(format='[%(asctime)s]-[%(levelname)s]-[%(name)s]: %(message)s', level=logging.DEBUG)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    title= db.Column(db.String(124), unique=True)
    price= db.Column(db.Integer)
    inventory_count= db.Column(db.Integer)

    def __init__(self, title, price, inventory_count):
        self.title = title
        self.price = price
        self.inventory_count = inventory_count

class ItemSchema(ma.Schema):
    class Meta:
        """
        Expose these fields in json
        """
        fields= ('title', 'price', 'inventory_count')

from routes.api import api_v1_bp
from routes.inventory import inventory


def add_access_control(response):
    '''
    Configures access-control for CORS.

    response: Flask.Reponse
        The response object which will be modified by this function.

    returns:
        The response object, modified with access-control headers.
    '''
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def create_app():
    '''
    Flask application factory.

    returns:
        A Flask configured application, with all registered endpoints, security
        headers and any other required features. But it won't be in running state!
    '''
 

    app.register_blueprint(api_v1_bp)
    app.after_request(add_access_control)


    return app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.secret_key = 'dev'
    app.run(host='0.0.0.0', port=PORT)