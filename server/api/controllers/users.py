# Python
from json import dumps
# Bottle
from bottle import request, response, hook, parse_auth
# Marshmallow
from marshmallow import ValidationError
# api
from api import app
from api.serializers import user_serializer
from api.models import db, User

from .authentication import encrypted_password, check_auth, user_token
from api.controllers.utilities import enable_cors


@hook('before_request')
def _connect_db():
    db.connect()


@hook('after_request')
def _close_db_and_enable_cors():
    enable_cors()
    if not db.is_closed():
        db.close()


@app.route(['/users/signup','/users/signup/'], method=['POST'])
def signup():
    req = request.json
    try:
        data = user_serializer.load(req)
    except ValidationError as err:
        response.content_type = 'application/json'
        response.status = 422
        return {'errors': err.messages}
    try:
        User.get(User.email == data['email'])
    except User.DoesNotExist:
        user = User.create(
            email=data['email'],
            password=encrypted_password(data['email'],data['password'])
        )
        message = f'Successfully created user: {user.email}'
    else:
        response.content_type = 'application/json'
        response.status = 400
        return {'errors': 'Invalid email. It is in use'}

    data = user_serializer.dump(user)
    data['message'] = message
    response.content_type = 'application/json'
    response.status = 201
    return data


@app.route(['/users/login','/users/login/'], method=['GET'])
def login():
    auth = request.get_header('Authorization')
    
    try:
        username, password = parse_auth(auth)
    except:
        response.content_type = 'application/json'
        response.status = 401
        resp = {'error': 'Empty credentials'}
        return dumps(resp)

    if check_auth(username, password):
        response.content_type = 'application/json'
        response.status = 200
        return dumps({'token': user_token(username)})

    response.content_type = 'application/json'
    response.status = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    resp = {'message': 'Authentication failed'}
    return dumps(resp)
