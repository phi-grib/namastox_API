from settings import *
from namastox import update
from flask import request

# PUT GENERAL_INFO
@app.route(f'{url_base}{version}general_info/<string:ra_name>',methods=['PUT'])
@cross_origin()
def updateGeneralInfo(ra_name):
    input_dict = request.form['general']
    success, data = update.action_update_general_info(ra_name, {'general':input_dict})
    if success:
        return data
    else:
        return f'Failed to update General Info for {ra_name} with error: {data}', 500

# PUT RESULT
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
