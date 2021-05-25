# Python
from functools import wraps
from json import dumps
# Bottle
from bottle import response, request, parse_auth
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
        auth = request.get_header('Authorization')
        try:
            username, password = parse_auth(auth)
        except:
            response.content_type = 'application/json'
            response.status = 401
            resp = {'error': 'Empty credentials'}
            return dumps(resp)
        if not auth or not check_auth(username, password):
            response.content_type = 'application/json'
            response.status = 401
            response.headers['WWW-Authenticate'] = 'Basic realm="Example"'
            resp = {'message': 'Authentication failed'}
            return dumps(resp)
        kwargs['user'] = User.get(User.email == username)
        return f(*args, **kwargs)

    return decorated
