import os
from flask import Flask
from flask import flash, jsonify, request, redirect, url_for, send_file
from flask_cors import CORS, cross_origin
from flask_sse import sse

UPLOAD_FOLDER = './'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'namastox misteries'
app.config["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://redis:6379/0")
app.register_blueprint(sse, url_prefix='/stream')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_base = "/namastox/"
version = "v1/"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'tsv', 'csv', 'doc', 'docx', 'xls', 'xlsx'}
ALLOWED_STRUCTURE_EXTENSIONS = {'sdf', 'mol', 'tsv', 'csv'}
ALLOWED_WORKFLOW_EXTENSIONS = {'csv'}
ALLOWED_IMPORT_EXTENSIONS = {'tgz'}
