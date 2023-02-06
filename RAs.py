from settings import *
from src import manage

# GET LIST of RA
@app.route(f'{url_base}{version}ra',methods=['GET'])
def getRAs():
    
    listRas = manage.action_list()
    return listRas
    
# GET SPECIFIC RA
@app.route(f'{url_base}{version}ra/<int:ra_name>',methods=['GET'])
def getRA(ra_name):
    return f'received ra number: {ra_name}'
