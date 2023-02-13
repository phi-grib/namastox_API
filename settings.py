from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
url_base = "/namastox/"
version = "v1/"