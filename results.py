from settings import *
from namastox import results

# GET RESULTS LIST of RA
@app.route(f'{url_base}{version}results/<string:ra_name>',methods=['GET'])
@app.route(f'{url_base}{version}results/<string:ra_name>/<int:step>',methods=['GET'])
@cross_origin()
def getResults(ra_name, step=None):
    success, data = results.action_results(ra_name, step, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain results for {ra_name} {step}', 500

@app.route(f'{url_base}{version}result/<string:ra_name>/<string:result_id>',methods=['GET'])
def getResult(ra_name, result_id):
    success, data = results.action_result(ra_name, result_id, out='json')
    if success:
        return data
    else:
        return f'Failed to obtain result {result_id} for {ra_name}', 500