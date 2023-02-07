from settings import *
from namastox import manage
from namastox import status
from namastox import results
from namastox import notes

# GET LIST of RA
@app.route(f'{url_base}{version}list',methods=['GET'])
def getList():
    success, data = manage.action_list(out='json')
    
    return data if success else ('Failed to obtain list of RA', 500)

# GET LIST of steps
@app.route(f'{url_base}{version}steps/<string:ra_name>',methods=['GET'])
def getSteps(ra_name):
    success, data = manage.action_steps(ra_name, out='json')
    
    return data if success else ('Failed to obtain steps for RA', 500)

# GET STATUS of RA
@app.route(f'{url_base}{version}status/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}status/<string:ra_name>/<int:step>',methods=['GET'])
def getStatus(ra_name, step=None):
    success, data = status.action_status(ra_name, step, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain status for {ra_name} {step}', 500

# GET GENERAL INFO RA
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['GET'])
def getGeneralInfo(ra_name):
    success, data = manage.action_info(ra_name, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain general info for {ra_name}', 500

# GET RESULTS LIST of RA
@app.route(f'{url_base}{version}results/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}results/<string:ra_name>/<int:step>',methods=['GET'])
def getResults(ra_name, step=None):
    success, data = results.action_results(ra_name, step, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain results for {ra_name} {step}', 500

@app.route(f'{url_base}{version}result/<string:ra_name>/<string:result_id>',methods=['GET'])
def getResult(ra_name, result_id):
    success, data = results.action_result(ra_name, result_id, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain result {result_id} for {ra_name}', 500

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