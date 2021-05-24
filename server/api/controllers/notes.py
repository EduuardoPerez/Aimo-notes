# Python
import os

# Bottle
from bottle import response

# api
from api import app
from api.models import Note, db
from api.serializers import notes_serializer


@app.route('/notes/', methods=['GET'])
def get_notes():
    db.init(os.getenv('DATABASE_PATH'))
    db.connect()
    notes = Note.select()  # Get all notes
    db.close()
    return notes_serializer.dump(list(notes))
