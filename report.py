from settings import *
from namastox import report
import json

# REPORT RA
@app.route(f'{url_base}{version}report/<string:ra_name>/<string:report_format>',methods=['GET'])
@cross_origin()
def reportRA(ra_name, report_format):
    success, report_file = report.action_report (ra_name, report_format)
    if success:
        return send_file(report_file, as_attachment=True)
    else:
        return json.dumps(f'Failed to report {ra_name}'), 500, {'ContentType':'application/json'} 