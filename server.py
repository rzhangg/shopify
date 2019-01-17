import os
import logging


from flask import Flask, g

from routes.api import api_v1_bp
from routes.inventory import inventory
from db import db
# from routes.classification import classification
# from routes.models_management import models_management

PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(format='[%(asctime)s]-[%(levelname)s]-[%(name)s]: %(message)s', level=logging.DEBUG)

app = Flask(__name__)

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
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.secret_key = "test"
    app.run(host='0.0.0.0', port=PORT)