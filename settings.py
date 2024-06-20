from flask import Flask
from flask_cors import CORS, cross_origin
from flask_session import Session  # Import Flask-Session
from authlib.integrations.flask_client import OAuth
import redis
import os
from dotenv import load_dotenv
UPLOAD_FOLDER = './'

app = Flask(__name__)
#replace conf with environment variables
# Cargar variables de entorno desde el archivo .env
load_dotenv()

appConf = {
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "REDIS_URL": "redis://localhost:6379/0"
}
app.secret_key = appConf.get("FLASK_SECRET")
# CONFIGURATION DEVELOPMENT
# app.config['SESSION_TYPE'] = 'filesystem'

#CONFIGURATION DEPLOYMENT
app.config['SESSION_TYPE'] = 'redis'
#Configure session cookies to be secure and HTTP-only. This helps prevent attacks such as XSS.
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(appConf.get("REDIS_URL"))

Session(app)  # Initialize Flask-Session
cors = CORS(app)
oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id= os.getenv('KEYCLOAK_CLIENT'),
    client_secret= os.getenv('KEYCLOAK_CLIENT_SECRET'),
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'{os.getenv("KEYCLOAK_URL")}/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration'
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
