from flask import Flask
from flask_cors import CORS, cross_origin
from flask_session import Session  # Import Flask-Session
from authlib.integrations.flask_client import OAuth
UPLOAD_FOLDER = './'

app = Flask(__name__)
appConf = {
    "OAUTH2_CLIENT_ID": "test_client",
    "OAUTH2_CLIENT_SECRET": "sRM7WdUDTJZfWcDAH1tMNB5vlPDooSoS",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/namastox",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 5000
}
app.secret_key = appConf.get("FLASK_SECRET")
# Configuration for storing sessions in the file system
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Initialize Flask-Session
cors = CORS(app)
oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration'
)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'namastox misteries'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_base = "/namastox/"
version = "v1/"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'tsv', 'csv', 'doc', 'docx', 'xls', 'xlsx'}
ALLOWED_STRUCTURE_EXTENSIONS = {'sdf', 'mol', 'tsv', 'csv'}
ALLOWED_WORKFLOW_EXTENSIONS = {'csv'}
ALLOWED_IMPORT_EXTENSIONS = {'tgz'}
