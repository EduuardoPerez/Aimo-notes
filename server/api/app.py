# Python
import os
# Bottle
from bottle import Bottle, hook, route, response
# Peewee
from peewee import SqliteDatabase


app = Bottle()
db = SqliteDatabase(os.getenv('DATABASE_PATH'))

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

def _enable_cors():
    """ Add headers to enable CORS """
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@app.hook('before_request')
def _before_request():
    db.connect()

@app.hook('after_request')
def _after_request():
    _enable_cors()
    if not db.is_closed():
        db.close()

@app.route('/<:re:.*>', method=['OPTIONS'])
def _enable_cors_generic_route():
    """ Add OPTIONS method to all routes to enable CORS """
    _enable_cors()
