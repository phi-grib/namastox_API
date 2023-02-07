from settings import *
from src import manage
from src import status

# GET LIST of RA
@app.route(f'{url_base}{version}list',methods=['GET'])
def getRAs():
    success, data = manage.action_list(out='json')
    if success:
        return data
    else:
        return 'Failed to obtain list of RA', 500

# GET LIST of steps
@app.route(f'{url_base}{version}steps/<string:ra_name>',methods=['GET'])
def getSteps(ra_name):
    success, data = manage.action_steps(ra_name, out='json')
    if success:
        return data
    else:
        return 'Failed to obtain steps for RA', 500

# GET SPECIFIC RA
@app.route(f'{url_base}{version}status/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}status/<string:ra_name>/<int:step>',methods=['GET'])
def getRA(ra_name, step=None):
    success, data = status.action_status(ra_name, step)
    if success:
        return data
    else:
        return f'Failed to obtain status for {ra_name} {step}', 500
