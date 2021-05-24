# Python
from functools import wraps
from json import dumps

# Bottle
from bottle import response, request

# Models
from api.models import User


def check_auth(email, password):
    """Check if a username/password combination is valid"""
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        return False
    return password == user.password


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers['Authorization']
        if not auth or not check_auth(auth.username, auth.password):
            response.content_type = 'application/json'
            response.status_code = 401
            response.headers['WWW-Authenticate'] = 'Basic realm="Example"'
            resp = {'message': 'Please authenticate'}
            return dumps(resp)
        kwargs['user'] = User.get(User.email == auth.username)
        return f(*args, **kwargs)

    return decorated
