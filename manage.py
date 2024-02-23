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
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain list of RAs'), 500, {'ContentType':'application/json'} 
    
# GET LIST of steps
@app.route(f'{url_base}{version}steps/<string:ra_name>',methods=['GET'])
@cross_origin()
def getSteps(ra_name):
    success, data = manage.action_steps(ra_name, out='json')
    
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain steps for RA {ra_name}'), 500, {'ContentType':'application/json'} 


# GET GENERAL INFO RA
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['GET'])
@cross_origin()
def getGeneralInfo(ra_name):
    success, data = manage.action_info(ra_name, out='json')
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain general infor for {ra_name}, with error {data}'), 500, {'ContentType':'application/json'} 

# PUT NEW RA
@app.route(f'{url_base}{version}new/<string:ra_name>',methods=['PUT'])
@cross_origin()
def putNew(ra_name):
    success, data = manage.action_new(ra_name)
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to create new RA {ra_name}, with error {data}'), 500, {'ContentType':'application/json'} 

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

# # PUT CUSTOM WORKFLOW DEFINITION
# @app.route(f'{url_base}{version}custom_workflow/<string:ra_name>',methods=['PUT'])
# @cross_origin()
# def putCustomWorkflow(ra_name, step=None):

#     # check if the post request has the file part
#     if 'file' not in request.files:
#         return json.dumps(f'Failed to upload file, no file information found'), 500, {'ContentType':'application/json'} 
    
#     file = request.files['file']
#     # If the user does not select a file, the browser submits an
#     # empty file without a filename.
#     if file.filename == '':
#         return json.dumps(f'Failed to upload file, empty file name'), 500, {'ContentType':'application/json'} 
    
#     if file and allowed_workflow(file.filename):
#         filename = secure_filename(file.filename)
#         success, ra_path = manage.getPath (ra_name)
#         if not success:
#             return json.dumps(f'Failed to upload file, unable to access repository'), 500, {'ContentType':'application/json'} 
#         file.save(os.path.join(ra_path, filename))
#         success, result = manage.setCustomWorkflow (ra_name, filename)
#     else:
#         return json.dumps(f'Failed to upload file, no file'), 500, {'ContentType':'application/json'} 
#     return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

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
        return json.dumps({"success": False, "error": "Failed to upload file, no file information found"}), 500, {'ContentType':'application/json'} 
    
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return json.dumps({"success": False, "error": "Failed to upload file, empty filename"}), 500, {'ContentType':'application/json'} 
    
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
    
# RETURN DOCUMENTATION FOR A MODELS
@app.route(f'{url_base}{version}model_documentation/<string:model_name>/<int:model_ver>',methods=['GET'])
@cross_origin()
def modelDocumentation(model_name, model_ver):
    success, models = manage.getModelDocumentation(model_name,model_ver)

    if success :
        return models, 200, {'ContentType':'application/json'}
    else:
        return json.dumps(f'Failed to get documentation for model {model_name} ver {model_ver}'), 500, {'ContentType':'application/json'} 
    
# PREDICT RA SUBSTANCE USING LIST OF MODELS
@app.route(f'{url_base}{version}predict/<string:ra_name>',methods=['PUT'])
@cross_origin()
def predict(ra_name):

    models = []
    versions = []

    if 'models' in request.form:
        models_raw = request.form['models'].strip().split(',')
        models = []
        for i in models_raw:
            if i!='':
                models.append(i)
    
    if 'versions' in request.form:
        versions_raw = request.form['versions'].strip().split(',')
        versions = []
        for i in versions_raw:
            if i!='':
                versions.append(int(i))

    if len(models)==0 or len(versions)==0 or len(versions)!=len(models):
        return json.dumps(f'Incomplete model information in prediction call'), 500, {'ContentType':'application/json'} 

    success, results = manage.predictLocalModels(ra_name, models, versions)
    if success:
        success, results = manage.getLocalModelPrediction()
        if success :
            return results, 200, {'ContentType':'application/json'}
        else:
            return json.dumps(f'Predictions not completed for substance of {ra_name}'), 500, {'ContentType':'application/json'} 
        
    else:
        return json.dumps(f'Failed to predict substance of {ra_name}'), 500, {'ContentType':'application/json'} 

# PREDICT RA SUBSTANCE USING LIST OF MODELS
@app.route(f'{url_base}{version}inform_name/<string:molname>',methods=['GET'])
@app.route(f'{url_base}{version}inform_casrn/<string:casrn>',methods=['GET'])
@cross_origin()
def inform(molname=None, casrn=None):
    success, results = manage.getInfoStructure(molname, casrn)

    if success:
        # the answer contains an structure like this:
        #[
        # {
        #     "activeAssays": 0,
        #     "averageMass": 68.075,
        #     "casrn": "110-00-9",
        #     "compoundId": 646,
        #     "cpdataCount": 2,
        #     "dtxcid": "DTXCID20646",
        #     "dtxsid": "DTXSID6020646",
        #     "genericSubstanceId": 20646,
        #     "hasStructureImage": true,
        #     "id": "FD7EFD3AFDFD6E00FD610A4EFD5C29FDFD2A3D3FFD4E3DFD3925FD39E7FD",
        #     "inchiKey": "YLQBMQCUIZJEEH-UHFFFAOYSA-N",
        #     "inchiString": "InChI=1S/C4H4O/c1-2-4-5-3-1/h1-4H\n",
        #     "isotope": 0,
        #     "iupacName": "Furan",
        #     "molFormula": "C4H4O",
        #     "monoisotopicMass": 68.026214749,
        #     "multicomponent": 0,
        #     "percentAssays": 0,
        #     "preferredName": "Furan",
        #     "pubchemCid": 8029,
        #     "pubchemCount": 280,
        #     "pubmedCount": 919,
        #     "qcLevel": 1,
        #     "qcLevelDesc": "Level 1: Expert curated, highest confidence in accuracy and consistency of unique chemical identifiers",
        #     "relatedStructureCount": 1,
        #     "relatedSubstanceCount": 1,
        #     "selected": null,
        #     "smiles": "O1C=CC=C1",
        #     "sourcesCount": 230,
        #     "stereo": 0,
        #     "totalAssays": 235,
        #     "toxcastSelect": "0/235"
        # }
        #]
        # the dtxsid can be used to present a link like this
        # https://comptox.epa.gov/dashboard/chemical/details/DTXSID4041280

        return results, 200, {'ContentType':'application/json'}
    else:
        return json.dumps(f'Failed to inform mol {molname} with error {results}'), 500, {'ContentType':'application/json'} 
