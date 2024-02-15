from settings import *
from namastox import notes
import json

# GET NOTES LIST of RA
@app.route(f'{url_base}{version}notes/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}notes/<string:ra_name>/<int:step>',methods=['GET'])
def getNotes(ra_name, step=None):
    success, data = notes.action_notes(ra_name, step, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain notes for {ra_name} {step}', 500

@app.route(f'{url_base}{version}note/<string:ra_name>/<string:note_id>',methods=['GET'])
def getNote(ra_name, note_id):
    success, data = notes.action_note(ra_name, note_id, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain note {note_id} for {ra_name}', 500
    
@app.route(f'{url_base}{version}note/<string:ra_name>',methods=['PUT'])
def putNote(ra_name):

    note = {}

    if 'note' in request.form:
        note['id'] = request.form['id']
        note['title'] = request.form['title']
        note['date'] = request.form['date']
        note['text'] = request.form['text']
    else:
        note = {'id':'MY', 'title':'MYTITLE', 'date':'MYDATE', 'text': 'MYTEXT'}

    success, data = notes.action_note_add(ra_name, note)
    if success:
        return data
    else:
        return f'Failed to add note to {ra_name}', 500