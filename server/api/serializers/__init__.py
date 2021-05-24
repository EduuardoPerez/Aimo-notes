from .users import *
from .notes import *

user_serializer = UserModelSerializer()
note_serializer = NoteModelSerializer()
notes_serializer = NoteModelSerializer(many=True)