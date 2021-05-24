# Bottle
from bottle import request, response

# Marshmallow
from marshmallow import ValidationError

# api
from api import app
from api.serializers import user_serializer
from api.models import User


@app.route(['/users/signup','/users/signup/'], method=['POST'])
def signup():
    req = request.json
    try:
        data = user_serializer.load(req)
    except ValidationError as err:
        response.status = 422
        return {'errors': err.messages}
    try:
        User.get(User.email == data['email'])
    except User.DoesNotExist:
        user = User.create(
            email=data['email'], password=data['password']
        )
        message = f'Successfully created user: {user.email}'
    else:
        response.status = 400
        return {'errors': 'Invalid email. It is in use'}

    data = user_serializer.dump(user)
    data['message'] = message
    response.status = 201
    return data
