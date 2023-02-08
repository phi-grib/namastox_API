from flask import Flask,jsonify
from flask_cors import CORS, cross_origin
# from flask_api import FlaskAPI
# from flask_api import status as Status
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
url_base = "/namastox/"
version = "v1/"