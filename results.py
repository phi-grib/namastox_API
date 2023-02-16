from settings import *
from namastox import results
import json

# GET RESULTS LIST of RA
@app.route(f'{url_base}{version}results/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}results/<string:ra_name>/<int:step>',methods=['GET'])
@cross_origin()
def getResults(ra_name, step=None):
    success, data = results.action_results(ra_name, step, out='json')
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain results for {ra_name} step {step} with error: {data}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}result/<string:ra_name>/<string:result_id>',methods=['GET'])
def getResult(ra_name, result_id):
    success, data = results.action_result(ra_name, result_id, out='json')
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain result {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
    
@app.route(f'{url_base}{version}pending_tasks/<ra_name>',methods=['GET'])
def getPendingTasks(ra_name):
    success, data = results.action_pendingTasks(ra_name)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain pending tasks for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}pending_task/<ra_name>/<string:result_id>',methods=['GET'])
def getPendingTask(ra_name, result_id):
    success, data = results.action_pendingTask(ra_name, result_id)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain pending task {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
