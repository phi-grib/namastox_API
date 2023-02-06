from settings import *
notes = [
      {
          "name":'Note1',
          "date":"21-02-2020"
      },
      {
          "name":"Note2",
          "date":"11-02-2021"
      }
  ]

# RA ROUTES

# GET LIST of RA
@app.route('/notes',methods=['GET'])
def getNotes():
    return jsonify(notes)

# GET SPECIFIC RA
@app.route('/ra/<int:note_name>',methods=['GET'])
def getNote(note_name):
    return f'received note number: {note_name}'
