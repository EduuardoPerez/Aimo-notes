# Marshmallow
from marshmallow import (
    Schema,
    fields,
    post_dump,
    post_load,
)
# Serializers
from .users import UserModelSerializer
# Models
from api.models import Note

class NoteModelSerializer(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserModelSerializer(
        exclude=('email', 'password')
        ),
        dump_only=True
    )

    # Adding an envelope to responses
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = 'notes' if many else 'note'
        return {key: data}

    @post_load
    def make_object(self, data, **kwargs):
        """create a new Note from validated data"""
        if not data:
            return None
        return Note(
            title=data['title'],
            content=data['content'],
        )
