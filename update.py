from settings import *
from user import checkAccess
import json
import os
from namastox import update
from namastox import manage
from flask import request
from werkzeug.utils import secure_filename

def allowed_attachment(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'csv'}

# PUT GENERAL_INFO
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['PUT'])
@cross_origin()
def updateGeneralInfo(ra_name):

    granted, access_result = checkAccess(ra_name,'write')
    if not granted:
        return access_result # this is the 403 JSON response

    input_string = request.form['general']
    input_dict = json.loads(input_string)

    # check if the post request has the file part
    if 'custom_workflow_file' in request.files:
        file = request.files['custom_workflow_file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file is None:
            return json.dumps(f'Failed to upload file, empty file nama'), 500, {'ContentType':'application/json'} 
        
        if file and allowed_attachment(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace (' ','_')
            success, data = manage.getPath (ra_name)
            if not success:
                return json.dumps(f'Failed to upload file, unable to access repository'), 500, {'ContentType':'application/json'} 

            file.save(os.path.join(data, filename))
            
            if not 'workflow_custom' in input_dict:
                input_dict['workflow_custom'] = filename

    success, data = update.action_update_general_info(ra_name, {'general':input_dict})
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to update General Info for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 

# PUT USERS
@app.route(f'{url_base}{version}users/<string:ra_name>',methods=['PUT'])
@cross_origin()
def updateUsers(ra_name):

    granted, access_result = checkAccess(ra_name,'write')
    if not granted:
        return access_result # this is the 403 JSON response

    users_read=None
    users_write=None
    if 'read' in request.form:
        users_read = request.form['read'].replace(' ', '').strip().split(',')
    if 'write' in request.form:
        users_write = request.form['write'].replace(' ', '').strip().split(',')

    manage.action_setusers(ra_name, users_read, users_write)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# PUT RESULT
@app.route(f'{url_base}{version}result/<string:ra_name>',methods=['PUT'])
@app.route(f'{url_base}{version}result/<string:ra_name>/<int:step>',methods=['PUT'])
@cross_origin()
def updateResult(ra_name, step=None):

    granted, access_result = checkAccess(ra_name,'write')
    if not granted:
        return access_result # this is the 403 JSON response

    input_string = request.form['result']
    input_dict = json.loads(input_string)
    success, data = update.action_update_result(ra_name, step, {'result':[input_dict]})
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to update Result for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
