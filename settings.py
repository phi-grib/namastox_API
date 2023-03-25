from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_api import FlaskAPI
from flask import flash, request, redirect, url_for, send_file

UPLOAD_FOLDER = './'

app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'namastox misteries'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_base = "/namastox/"
version = "v1/"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_STRUCTURE_EXTENSIONS = {'sdf', 'mol', 'tsv', 'csv'}
