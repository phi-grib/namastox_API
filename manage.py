from settings import *
from namastox import manage

# CREATE NEW RA
@app.route(f'{url_base}{version}new/<string:ra_name>',methods=['GET'])
@cross_origin()
def newRA(ra_name):
    success, data = manage.action_new(ra_name)
    
    return data if success else (f'Failed to create new RA {ra_name}', 500)

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
        return f'Failed to obtain general info for {ra_name}', 500
