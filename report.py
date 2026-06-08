from settings import *
from user import getUsername, checkAccess
from namastox import report
import json

# REPORT RA
@app.route(f'{url_base}{version}report/<string:ra_name>/<string:report_format>',methods=['GET'])
@cross_origin()
def reportRA(ra_name, report_format):
    username = getUsername()
    granted, access_result = checkAccess(ra_name, username, 'read')
    if not granted:
        return access_result # this is the 403 JSON response

    success, result = report.action_report (ra_name, username, report_format)
    if success:
        return send_file(result, as_attachment=True)
    else:
        return json.dumps(f'Failed to report {ra_name}, with error: {result}'), 500, {'ContentType':'application/json'} 