# Python
import os
# Bottle
from bottle import response, request
# Marshmallow
from marshmallow import ValidationError
# api
from api import app
from api.models import Note
from api.serializers import notes_serializer, note_serializer
from api.authentication import requires_auth


@app.route(['/notes','/notes/'], method=['GET'])
@requires_auth
def get_notes(user):
    notes = Note.select().where(Note.user == user)
    response.content_type = 'application/json'
    response.status = 200
    return notes_serializer.dump(list(notes))


@app.route(['/notes','/notes/'], method=['POST'])
@requires_auth
def new_note(user):
    content = request.json
    try:
        note = note_serializer.load(content)
    except ValidationError as err:
        response.status = 422
        response.content_type = 'application/json'
        return {"errors": err.messages}
    note.user = user
    note.save()
    response.content_type = 'application/json'
    response.status = 201
    return note_serializer.dump(note)
