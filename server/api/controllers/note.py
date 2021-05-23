from api import app
from bottle import request, response
from api.models import Note
from json import dumps


@app.route('/', method=['GET','POST'])
def index():
    return 'Hello world!'

@app.route(['/note','/note/'], method='POST')
def create_note():
    title = request.json['title']
    content = request.json['content']
    owner_id = request.json['owner_id']
    note = Note(title=title,content=content,owner=owner_id)
    note.save()

@app.route(['/notes','/notes/'], method='GET')
def list_notes():
    notes = list(Note.select())
    resp = []
    for note in notes:
        dict_note = {
            'title': note.title,
            'content': note.content,
            'owner_id': note.owner.id
        }
        resp.append(dict_note)
    response.content_type = 'application/json'
    return dumps(resp)
