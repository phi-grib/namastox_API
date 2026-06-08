from settings import *
from user import getUsername, checkAccess
from namastox import results
import json

# GET RESULTS LIST of RA
@app.route(f'{url_base}{version}results/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}results/<string:ra_name>/<int:step>',methods=['GET'])
@cross_origin()
def getResults(ra_name, step=None):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = results.action_results(ra_name, username, step, out='json')
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain results for {ra_name} step {step} with error: {data}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}result/<string:ra_name>/<string:result_id>',methods=['GET'])
@cross_origin()
def getResult(ra_name, result_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = results.action_result(ra_name, username, result_id, out='json')
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain result {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
    
@app.route(f'{url_base}{version}task/<string:ra_name>/<string:result_id>',methods=['GET'])
@cross_origin()
def getTask(ra_name, result_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = results.action_task(ra_name, username, result_id)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain task {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}pending_tasks/<ra_name>',methods=['GET'])
@cross_origin()
def getPendingTasks(ra_name):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response
    
    success, data = results.action_pendingTasks(ra_name, username)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain pending tasks for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 

@app.route(f'{url_base}{version}pending_task/<ra_name>/<string:result_id>',methods=['GET'])
@cross_origin()
def getPendingTask(ra_name, result_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response

    success, data = results.action_pendingTask(ra_name, username, result_id)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain pending task {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 


@app.route(f'{url_base}{version}upstream_tasks/<ra_name>/<string:result_id>',methods=['GET'])
@cross_origin()
def getUpstreamTasks(ra_name, result_id):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response

    success, data = results.action_upstreamTasks(ra_name, username, result_id)
    if success:
        return data
    else:
        return json.dumps(f'Failed to obtain upstream tasks of {result_id} for {ra_name} with error: {data}'), 500, {'ContentType':'application/json'} 
