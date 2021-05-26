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


@app.hook('before_request')
def _before_request():
    db.connect()

@app.hook('after_request')
def _after_request():
    '''Add headers to enable CORS and close db connection'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

    if not db.is_closed():
        db.close()
