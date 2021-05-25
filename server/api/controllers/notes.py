# Python
import os
# Bottle
from bottle import response, request
# Marshmallow
from marshmallow import ValidationError
# api
from api import app
from api.models import Note, db
from api.serializers import notes_serializer, note_serializer
from api.controllers.utilities import requires_auth


@app.route(['/notes','/notes/'], method=['GET'])
def get_notes():
    notes = Note.select()  # Get all notes
    return notes_serializer.dump(list(notes))


@app.route(['/notes','/notes/'], method=['POST'])
@requires_auth
def new_note(user):
    content = request.json
    try:
        note = note_serializer.load(content)
    except ValidationError as err:
        response.status = 422
        return {"errors": err.messages}
    note.user = user
    note.save()
    return note_serializer.dump(note)