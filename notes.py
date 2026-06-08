from settings import *
from user import getUsername, checkAccess
from namastox import notes
import json

# GET NOTES LIST of RA
@app.route(f'{url_base}{version}notes/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}notes/<string:ra_name>/<int:step>',methods=['GET'])
def getNotes(ra_name, step=None):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = notes.action_notes(ra_name, username, step, out='json')
    if success:
        return json.dumps(data), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to obtain notes for {ra_name} {step}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}note/<string:ra_name>/<string:note_id>',methods=['GET'])
def getNote(ra_name, note_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response

    success, data = notes.action_note(ra_name, username, note_id)
    if success:
        return json.dumps(data), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to obtain note {note_id} for {ra_name}'), 500 , {'ContentType':'application/json'} 
    
@app.route(f'{url_base}{version}note/<string:ra_name>',methods=['PUT'])
def putNote(ra_name):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'write')
    if not granted:
        return access_result # this is the 403 JSON response
    
    note = {}
    if 'title' in request.form and 'text' in request.form :
        note['title'] = request.form['title']
        note['text'] = request.form['text']
    else:
        return json.dumps('No note found'), 500, {'ContentType':'application/json'} 

    success, data = notes.action_note_add(ra_name, username, note)
    if success:
        return json.dumps(data), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to add note to {ra_name}'), 500, {'ContentType':'application/json'} 
    
@app.route(f'{url_base}{version}note/<string:ra_name>/<string:note_id>',methods=['DELETE'])
def deleteNote(ra_name, note_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'write')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = notes.action_note_delete(ra_name, username, note_id)
    if success:
        return json.dumps(data), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to delete note {note_id} note to {ra_name}'), 500, {'ContentType':'application/json'} 