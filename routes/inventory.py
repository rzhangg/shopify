import os
import itertools
import logging

from flask import Response, request, jsonify
from flask_restplus import Resource, fields

from routes.api import api
import json

logger = logging.getLogger('inventory')
inventory = api.namespace('inventory', description='Inventory')

@inventory.route('')
@api.doc(responses = {
            200: 'Success',
            404: 'Not Found',
            500: 'Internal Server Error'
        })

class Inventory(Resource):
    """
    Gets Inventory
    """

    def get(self):
        resp = Response()
        resp.mimetype = 'application/json'
        resp = jsonify('test')
        resp.status_code = 200

        return resp