# Bottle
from bottle import request

# Marshmallow
from marshmallow import ValidationError

from api import app
from api.serializers import user_serializer
from api.models import User

@app.route('/register', method=['POST'])
def register():
    req = request.json()
    try:
        data = user_serializer.load(req)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    try:
        User.get(User.email == data['email'])
    except User.DoesNotExist:
        user = User.create(
            email=data['email'], password=data['password']
        )
        message = f'Successfully created user: {user.email}'
    else:
        return {'errors': 'Invalid email. It is in use'}, 400

    data = user_serializer.dump(user)
    data['message'] = message
    return data, 201
