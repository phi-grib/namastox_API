from flask import Blueprint, session, redirect, url_for, abort,jsonify,render_template
from urllib.parse import quote_plus, urlencode
from settings import *
import requests
import json
from flask import request
from dotenv import load_dotenv
import os
import logging
from functools import wraps
import jwt
from user import getUsername
auth_routes = Blueprint('auth_routes', __name__)
load_dotenv() # load env variables

logging.basicConfig(level=logging.DEBUG) # Basic logging configuration

@app.route("/")
def index():
    if "user" in session:
        return app.send_static_file('index.html')
    else:
        return redirect(url_for('login'))
    
# Decorator for required login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/protected")
@login_required
def protected():
    return "You have access to this protected route"

@app.route("/namastox/v1/user_info/")
@login_required
def user_info():
    return json.dumps({'username':getUsername()}), 200, {'ContentType':'application/json'} 

@app.route('/login')
def login():
    authorize_url = f"{os.environ.get('KEYCLOAK_AUTHORIZE_URL')}/realms/{os.environ.get('KEYCLOAK_REALM')}/protocol/openid-connect/auth"
    redirect_uri = f"{os.environ.get('DOMAIN_WEB_URL')}/callback"
    params = {
        'client_id':os.environ.get('KEYCLOAK_CLIENT'),
        'redirect_uri':redirect_uri,
        'response_type': 'code',
        'scope': 'openid profile email'
    }
    return redirect(f"{authorize_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    logging.debug(f"Callback received with code:{code}")
    token_endpoint = f"{os.environ.get('KEYCLOAK_URL')}/realms/{os.environ.get('KEYCLOAK_REALM')}/protocol/openid-connect/token"
    payload = {
        "grant_type": "authorization_code",
        "code":code,
        "redirect_uri": f"{os.environ.get('DOMAIN_WEB_URL')}/callback",
        "client_id": os.environ.get('KEYCLOAK_CLIENT'),
        "client_secret":os.environ.get('KEYCLOAK_CLIENT_SECRET')
    }
    logging.debug(f"Token request payload: {payload}")
    try:
        response = requests.post(token_endpoint,data=payload,verify=False)
        if response.status_code != 200:
            logging.error(f"Error fetching tokens: {response.status_code} - {response.text}")
            return "Failed to fetch tokens."

        token_data = response.json()
        decoded_token = jwt.decode(token_data['access_token'],options={"verify_signature":False})
        if "access_token" in token_data:
            session['user'] = {
                "username": decoded_token["preferred_username"],
            }

            logging.debug("User logged in successfully.")
            return redirect(url_for('index'))
        else:
            logging.error("Failed to fetch tokens.")
            return "Failed to fetch tokens."
    except Exception as e:
        logging.error(f"Exception during token exchange: {e}")
        return "Failed to fetch tokens"

@app.route("/logout")
def logout():
    logging.debug("Attempting to logout...")
    session.clear()
    logout_url = f"{os.environ.get('KEYCLOAK_AUTHORIZE_URL')}/realms/{os.environ.get('KEYCLOAK_REALM')}/protocol/openid-connect/logout?redirect_uri={url_for('index',_external=True)}"
    return redirect(logout_url)


