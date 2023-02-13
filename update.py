from settings import *
from namastox import update
from flask import request
import json

# GET RESULTS LIST of RA
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['PUT'])
@cross_origin()
def updateGeneralInfo(ra_name):
    #TODO extract input_dict from payload
    input_dict = {}
    success, data = update.action_update_general_info(ra_name, input_dict)
    if success:
        return data
    else:
        return f'Failed to update General Info for {ra_name} with error: {data}', 500

@app.route(f'{url_base}{version}result/<string:ra_name>',methods=['PUT'])
@app.route(f'{url_base}{version}result/<string:ra_name>/<int:step>',methods=['PUT'])
@cross_origin()
def updateResult(ra_name, step=None):
    input_dict = request.form['result']
    success, data = update.action_update_result(ra_name, step, [{'result':input_dict}])
    if success:
        return data
    else:
        return f'Failed to update Result for {ra_name} step {step} with error: {data}', 500
