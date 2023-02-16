from settings import *
from namastox import update
from flask import request
import json

# PUT GENERAL_INFO
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['PUT'])
@cross_origin()
def updateGeneralInfo(ra_name):
    input_string = request.form['general']
    input_dict = json.loads(input_string)
    success, data = update.action_update_general_info(ra_name, {'general':input_dict})
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to update General Info for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 

# PUT RESULT
@app.route(f'{url_base}{version}result/<string:ra_name>',methods=['PUT'])
@app.route(f'{url_base}{version}result/<string:ra_name>/<int:step>',methods=['PUT'])
@cross_origin()
def updateResult(ra_name, step=None):
    input_string = request.form['result']
    input_dict = json.loads(input_string)
    success, data = update.action_update_result(ra_name, step, {'result':[input_dict]})
    if success:
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps(f'Failed to update Result for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
