from settings import *
from namastox import manage
import json
import os
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
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

    success, results = manage.action_get_link(ra_name, link_name)

    if success:
        return send_file(link_name, mimetype=None, as_attachment=False, 
                  download_name=None, conditional=True, etag=True, last_modified=None, max_age=None)

        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to get link {link_name}, with error {response}'), 500, {'ContentType':'application/json'} 
