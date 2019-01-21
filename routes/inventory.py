import os
import itertools
import logging

from flask import Response, request, jsonify
from flask_restplus import Resource, reqparse
from routes.api import api

logger = logging.getLogger('inventory')
inventory = api.namespace('inventory', description='Inventory')
from server import db,Item, ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@inventory.route('/getall/<int:inventory_count>')
@api.doc(responses = {
            200: 'Success',
            401: 'Negative inventory levels',
            400: 'No entries',
            500: 'Internal Server Error'
        })

class GetInventory(Resource):
    """
    Queries database for all Items from SQLite. 
    """
    @api.doc(description='gets all items from database with inventory more than inventory_count(0 means get all items)')
    def get(self,inventory_count):
        logger.debug('Getting inventory')
        resp = Response()
        resp.mimetype = 'application/json'
        if inventory_count < 0:
            logger.error('Entered negative inventory levels')
            resp = jsonify({'message':'entered negative inventory levels'})
            resp.status_code = 401
            return resp
        all_items = Item.query.filter(Item.inventory_count>= inventory_count).all() 
        result = items_schema.dump(all_items)
        if result is None:
            logger.error('No items in database')
            resp = jsonify({'message':'error getting items'} )
            resp.status = 400
        else:
            resp = jsonify(result)
            logger.info(result)
            resp.status_code = 200
        return resp

@inventory.route('/getitem/<string:title>')
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
        item = Item.query.filter(Item.title == title).all() 
        result = items_schema.dumps(item)
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
    400:'Item exists',
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
        item = Item.query.filter(Item.title == title).all() 
        #check len of item object because item will exists even if there is nothing found
        if len(item) is not 0:
            logger.error('item exists')
            resp.status_code = 400
            resp = jsonify({'message': 'item already exists'})
            return resp
        else:
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

@inventory.route('/buy/<string:title>%<int:inventory_count>')
@api.doc(response = {
    200:'Succress',
    401:'No item found',
    400:'Item not enough inventory',
    500:'Internal server error'
})
class PurchaseItem(Resource):
    """
    Purchasing an item in the database, throw error when item does not have enough inventory"
    """
    @api.doc(description='Purchase an item by title. Purchases are only valid if they have enough inventory')
    def put(self,title,inventory_count):
        logger.debug('Purchasing new item')
        resp = Response()
        resp.mimetype= 'application/json'
        item = Item.query.filter(Item.title == title).all()
        #checking if len is 0 meaning that item is not found
        if len(item) is 0:
            logger.error('no item found')
            resp = jsonify({'message': 'no item found'})
            resp.status_code = 401
            return resp
        temp_item = items_schema.dumps(item)
        logger.info(temp_item)
        inv_count = item[0].inventory_count
        if inventory_count > inv_count:
            logger.error('not enough inventory')
            resp = jsonify({'message': f'purchase exceeds item:{title} inventory levels'})
            resp.status_code = 400
            return resp
        else:
            try: 
                new_inv = inv_count - inventory_count
                logger.info(f'new inventory level: {new_inv}')
                item[0].inventory_count = inv_count - inventory_count
                db.session.commit()
                resp = jsonify({'message': 'purchase OK!', 'title':f'{title}', 'new inventory':f'{new_inv}'})
                resp.status_code = 200
                return resp
            except:
                logger.error('Error commiting purchase')
                resp.status_code = 500
                resp = jsonify({'message':'error commiting purchase'})
                return resp