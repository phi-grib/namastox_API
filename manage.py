from settings import *
from namastox import manage
import json

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
