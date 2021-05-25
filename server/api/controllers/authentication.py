# Python
import os
from functools import wraps
from json import dumps
# Bottle
from bottle import response, request, parse_auth
#PyJWT
import jwt
# Models
from api.models import User


SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM='HS256'


def user_token(email):
    return jwt.encode({'user': email}, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token):
    """ Verify if the token is valid and search the user """
    try:
        jwt_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
    email = jwt_decode['user']
    try:
        user = User.get(User.email == email)
    except:
        return None
    return user


def encrypted_password(email, password):
    return jwt.encode({'user': email}, password, algorithm=ALGORITHM)


def check_auth(email, password):
    """Check if a username/password combination is valid"""
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        return False
    return encrypted_password(email, password) == user.password


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.get_header('Authorization')  
        
        try:
            token = str(auth).split('Token ')[1]
        except:
            response.content_type = 'application/json'
            response.status = 401
            resp = {'error': 'Invalid request. Check the user token credential syntax'}
            return dumps(resp)
        
        user = get_user_from_token(token)
        if not user:
            response.content_type = 'application/json'
            response.status = 401
            resp = {'error': 'Invalid request. Check the user token'}
            return dumps(resp)
        kwargs['user'] = user
        return f(*args, **kwargs)

    return decorated
