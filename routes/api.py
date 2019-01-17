from flask import Blueprint, url_for
from flask_restplus import Api, Resource, fields

api_v1_bp = Blueprint('api', __name__, url_prefix='/gshop/api/v1')
api = Api(api_v1_bp, version='1.0', doc='/doc/',
          security='', title='GSHOP APIs',
          description='Version 1.0 APIs for Grecko Shop')