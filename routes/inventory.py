import os
import itertools
import logging

from flask import Response, request, jsonify
from flask_restplus import Resource, fields
from routes.api import api

logger = logging.getLogger('inventory')
inventory = api.namespace('inventory', description='Inventory')
from server import db,Item, ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

upload_parser = api.parser()
upload_parser.add_argument('title',type=str, required=True, help='title')
upload_parser.add_argument('price',type=int, required=True, help='price')
upload_parser.add_argument('unit',type=int, required=True, help='unit')

@inventory.route('/all')
@api.doc(responses = {
            200: 'Success',
            404: 'Not Found',
            400: 'No entries',
            500: 'Internal Server Error'
        })

class Inventory(Resource):
    """
    Queries database for all Items from SQLite. 
    """
    @api.doc(description='gets all items from database')
    def get(self):
        logger.debug('Getting inventory')
        resp = Response()
        resp.mimetype = 'application/json'
        all_items = Item.query.all() 
        result = items_schema.dump(all_items)
        if result is None:
            logger.error('No items in database')
            resp = jsonify('error')
            resp.status = 400
        else:
            resp = jsonify(result)
            resp.status_code = 200
        return resp

@inventory.route('')
@api.doc(response = {
    200:'Succress',
    400:'Duplicate',
    500:'Internal server error'
})
class CreateItem(Resource):
    """
    For creating new item and adding it to SQLite"
    """
    @api.doc(description='add new item')
    @api.expect(upload_parser)
    def post(self):
        logger.debug('Adding new Item')
        resp = Response()
        resp.mimetype= 'application/json'
        req = request.data
        
        # title = request.json['title']
        # price = request.json['price']
        # units = request.json['units']
        print(req)
        new_item = Item(req)

        try:
            logger.info('commiting new Item to db')
            db.session.add(new_item)
            db.session.commit()
            resp = jsonify(new_item)
            resp.status_code = 200
            return resp
        except:
            logger.error('Error commiting Item')
            resp.status_code = 500
            resp = jsonify(new_item)
            return resp