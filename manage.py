from settings import *
from namastox import manage

import json
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename

# GET LIST of RA
@app.route(f'{url_base}{version}list',methods=['GET'])
@cross_origin()
def getList():
    success, data = manage.action_list(out='json')
    
    return data if success else ('Failed to obtain list of RA', 500)

# GET LIST of steps
@app.route(f'{url_base}{version}steps/<string:ra_name>',methods=['GET'])
@cross_origin()
def getSteps(ra_name):
    success, data = manage.action_steps(ra_name, out='json')
    
    return data if success else ('Failed to obtain steps for RA', 500)

# GET GENERAL INFO RA
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['GET'])
@cross_origin()
def getGeneralInfo(ra_name):
    success, data = manage.action_info(ra_name, out='json')
    if success:
        return data
    else:
        return json.dumps({f'Failed to obtain general infor for {ra_name}, with error {data}'}), 500, {'ContentType':'application/json'} 

# PUT NEW RA
@app.route(f'{url_base}{version}new/<string:ra_name>',methods=['PUT'])
@cross_origin()
def putNew(ra_name):
    success, data = manage.action_new(ra_name)
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps({f'Failed to create new RA {ra_name}, with error {data}'}), 500, {'ContentType':'application/json'} 

# PUT DELETE RA
@app.route(f'{url_base}{version}delete/<string:ra_name>',methods=['PUT'])
@app.route(f'{url_base}{version}delete/<string:ra_name>/<int:step>',methods=['PUT'])
@cross_origin()
def putKill(ra_name, step=None):
    success, data = manage.action_kill(ra_name, step)

    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        # return (f'failed for {ra_name}', 500)
        return json.dumps(f'Failed to delete RA {ra_name}, with error {data}'), 500, {'ContentType':'application/json'} 

def allowed_attachment(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_structure(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_STRUCTURE_EXTENSIONS

def allowed_workflow(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_WORKFLOW_EXTENSIONS

def allowed_import(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMPORT_EXTENSIONS


# PUT LINK, call this to send a link from the GUI to upload to the backend (RA repository)
@app.route(f'{url_base}{version}link/<string:ra_name>',methods=['POST'])
@cross_origin()
def putLink(ra_name):

    # check if the post request has the file part
    if 'file' not in request.files:
        return json.dumps(f'Failed to upload file, no file information found'), 500, {'ContentType':'application/json'} 
    
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return json.dumps(f'Failed to upload file, empty file nama'), 500, {'ContentType':'application/json'} 
    
    if file and allowed_attachment(file.filename):
        filename = secure_filename(file.filename)
        filename = filename.replace (' ','_')
        success, data = manage.getRepositoryPath (ra_name)
        if not success:
            return json.dumps(f'Failed to upload file, unable to access repository'), 500, {'ContentType':'application/json'} 

        file.save(os.path.join(data, filename))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to upload file, incorrect file or file type '), 500, {'ContentType':'application/json'} 

# GET LINK
@app.route(f'{url_base}{version}link/<string:ra_name>/<string:link_name>',methods=['GET'])
@cross_origin()
def getLink(ra_name, link_name):

    success, repo_path = manage.getRepositoryPath (ra_name)
    if success:
        link_name = link_name.replace (' ','_')
        link_file = os.path.join (repo_path, link_name)
        return send_file(link_file, as_attachment=True)
    else:
        return json.dumps(f'Failed to get link {link_name}, with error {repo_path}'), 500, {'ContentType':'application/json'} 

# GET WORKFLOW DEFINITION
@app.route(f'{url_base}{version}workflow/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}workflow/<string:ra_name>/<int:step>',methods=['GET'])
@cross_origin()
def getWorkflow(ra_name, step=None):
    success, workflow_graph = manage.getWorkflow (ra_name, step)
    if success:
        return json.dumps({'success':True, 'result': workflow_graph}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to get workflow for {ra_name}, with error {workflow_graph}'), 500, {'ContentType':'application/json'} 

# PUT CUSTOM WORKFLOW DEFINITION
@app.route(f'{url_base}{version}custom_workflow/<string:ra_name>',methods=['PUT'])
@cross_origin()
def putCustomWorkflow(ra_name, step=None):

    # check if the post request has the file part
    if 'file' not in request.files:
        return json.dumps(f'Failed to upload file, no file information found'), 500, {'ContentType':'application/json'} 
    
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return json.dumps(f'Failed to upload file, empty file nama'), 500, {'ContentType':'application/json'} 
    
    if file and allowed_workflow(file.filename):
        filename = secure_filename(file.filename)
        success, ra_path = manage.getPath (ra_name)
        if not success:
            return json.dumps(f'Failed to upload file, unable to access repository'), 500, {'ContentType':'application/json'} 
        file.save(os.path.join(ra_path, filename))
        # success, result = manage.setCustomWorkflow (ra_name, filename)
    else:
        return json.dumps(f'Failed to upload file, no file'), 500, {'ContentType':'application/json'} 
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# GET SUBSTANCE LIST
@app.route(f'{url_base}{version}substances',methods=['PUT'])
@cross_origin()
def convertSubstances():
    # check if the post request has the file part
    if 'file' not in request.files:
        return json.dumps(f'Failed to upload file, no file information found'), 500, {'ContentType':'application/json'} 
    file = request.files['file']

    if file and allowed_structure(file.filename):
        
        # copy the file to a temporary file in the backend 
        tempdirname = tempfile.mkdtemp()
        filename = secure_filename(file.filename)
        structure_path = os.path.join(tempdirname, filename)
        file.save(structure_path)

        # now call an endpoint which returns a JSON with the structure characteristics
        success, substances = manage.convertSubstances(structure_path)

        # remove the temp dir
        shutil.rmtree(tempdirname)

    else:
        return json.dumps(f'Failed to convert substances. Format unsuported'), 500, {'ContentType':'application/json'} 

    if success:
        return json.dumps({'success':True, 'result': substances}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to convert substances with error {substances}'), 500, {'ContentType':'application/json'} 

# EXPORT RA
@app.route(f'{url_base}{version}export/<string:ra_name>/',methods=['GET'])
@cross_origin()
def exportRA(ra_name):
    success, export_file = manage.exportRA (ra_name)
    if success:
        return send_file(export_file, as_attachment=True)
    else:
        return json.dumps(f'Failed to export {ra_name}'), 500, {'ContentType':'application/json'} 
    
# IMPORT RA
@app.route(f'{url_base}{version}import/',methods=['POST'])
@cross_origin()
def importRA():
    # check if the post request has the file part
    if 'file' not in request.files:
        return json.dumps(f'Failed to upload file, no file information found'), 500, {'ContentType':'application/json'} 
    
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return json.dumps(f'Failed to upload file, empty file nama'), 500, {'ContentType':'application/json'} 
    
    if file and allowed_import(file.filename):

        # copy the file to a temporary file in the backend 
        tempdirname = tempfile.mkdtemp()
        filename = secure_filename(file.filename)
        import_path = os.path.join(tempdirname, filename)
        file.save(import_path)

        # call import with local path pointing to temp dir
        success, message = manage.importRA (import_path)

        # remove the temp dir
        shutil.rmtree(tempdirname)

        if not success:
            return json.dumps(f'Failed to import file {import_path} with error: {message}'), 500, {'ContentType':'application/json'} 

    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to import {filename}'), 500, {'ContentType':'application/json'} 
    
# RETURN LIST OF LOCALLY ACCESSIBLE MODELS
@app.route(f'{url_base}{version}models/',methods=['GET'])
@cross_origin()
def localModels():
    success, models = manage.getLocalModels()

    if success :
        return models, 200, {'ContentType':'application/json'}
    else:
        return json.dumps(f'Failed to get list of local models'), 500, {'ContentType':'application/json'} 
    
# PREDICT RA SUBSTANCE USING LIST OF MODELS
@app.route(f'{url_base}{version}predict/<string:ra_name>',methods=['GET'])
@cross_origin()
def predict(ra_name):

    success, results = manage.predictLocalModels(ra_name, ['AMPA','AMPA'], [1,2])
    if success :
        return results, 200, {'ContentType':'application/json'}
    else:
        return json.dumps(f'Failed to predict substance of {ra_name}'), 500, {'ContentType':'application/json'} 

    
   