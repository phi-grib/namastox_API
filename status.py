from settings import *
from namastox import status

# GET STATUS of RA
@app.route(f'{url_base}{version}status/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}status/<string:ra_name>/<int:step>',methods=['GET'])
@cross_origin()
def getStatus(ra_name, step=None):
    success, data = status.action_status(ra_name, step, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain status for {ra_name} {step}', 500
