# Python
import os
# Bottle
from bottle import response, request, hook
# Marshmallow
from marshmallow import ValidationError
# api
from api import app
from api.models import db, Note
from api.serializers import notes_serializer, note_serializer
from api.controllers.authentication import requires_auth


@hook('before_request')
def _connect_db():
    db.connect()


@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()


@app.route(['/notes','/notes/'], method=['GET'])
@requires_auth
def get_notes(user):
    notes = Note.select().where(Note.user == user)
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
