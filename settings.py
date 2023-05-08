from flask import Flask
from flask import flash, jsonify, request, redirect, url_for, send_file
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = './'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'namastox misteries'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_base = "/namastox/"
version = "v1/"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_STRUCTURE_EXTENSIONS = {'sdf', 'mol', 'tsv', 'csv'}
ALLOWED_WORKFLOW_EXTENSIONS = {'csv'}
ALLOWED_IMPORT_EXTENSIONS = {'tgz'}
