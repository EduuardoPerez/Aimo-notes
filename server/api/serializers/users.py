# Marshmallow
from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    post_dump,
)

class UserModelSerializer(Schema):
    """Serializer for User model"""
    id = fields.Int(dump_only=True)
    email = fields.Str(
        required=True,
        validate=validate.Email(error='Not a valid email address')
    )
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=36)],
        load_only=True
    )

    # Cleanning data
    @pre_load
    def process_input(self, data, **kwargs):
        data['email'] = data['email'].lower().strip() # lowercase and without leading and trailing whitespaces
        return data

    # Adding a post_dump hook to add an envelope to responses
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = 'users' if many else 'user'
        return {key: data}
