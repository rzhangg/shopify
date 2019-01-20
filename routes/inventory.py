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

@inventory.route('/get')
@api.doc(responses = {
            200: 'Success',
            404: 'Not Found',
            400: 'No entries',
            500: 'Internal Server Error'
        })

class GetInventory(Resource):
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
            resp = resp = jsonify({'message':'error getting items'} )
            resp.status = 400
        else:
            resp = jsonify(result)
            logger.info(result)
            resp.status_code = 200
        return resp

@inventory.route('/<string:title>')
@api.doc(responses = {
            200: 'Success',
            404: 'Not Found',
            400: 'No entries',
            500: 'Internal Server Error'
        })

class GetItem(Resource):
    """
    Queries database for specific item by title from SQLite db. 
    """
    @api.doc(description='get item by title')
    def get(self, title):
        logger.debug(f'Getting {title}')
        resp = Response()
        resp.mimetype = 'application/json'
        item = Item.query.get(1) 
        result = item_schema.dumps(item)
        if result is None:
            logger.error(f'No item named {title} found in database')
            resp = jsonify({'message':'error getting item'} )
            resp.status = 400
        else:
            resp = jsonify(result)
            logger.info(result)
            resp.status_code = 200
        return resp

@inventory.route('/<string:title>&<int:price>&<int:inventory_count>')
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
    def post(self,title,price,inventory_count):
        logger.debug('Adding new Item')
        resp = Response()
        resp.mimetype= 'application/json'
        logger.info(f'title: {title} price:{price} inventory_count:{inventory_count}')
        new_item = Item(title,price,inventory_count)

        try:
            logger.info('commiting new Item to db')
            logger.info(new_item)
            db.session.add(new_item)
            db.session.commit()
            resp = jsonify(item_schema.dump(new_item))
            resp.status_code = 200
            return resp
        except:
            logger.error('Error commiting Item')
            resp.status_code = 500
            resp = jsonify({'message':'error commiting item'})
            return resp