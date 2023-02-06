from settings import *
from src import manage
from src import status

# GET LIST of RA
@app.route(f'{url_base}{version}list',methods=['GET'])
def getRAs():
    success, data = manage.action_list(out='json')
    return data

    
# GET SPECIFIC RA
@app.route(f'{url_base}{version}status/<string:ra_name>',methods=['GET'])
def getRA(ra_name):
    success, data = status.action_status(ra_name)
    return data
