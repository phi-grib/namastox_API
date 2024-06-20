from flask import Blueprint, session, redirect, url_for, abort,jsonify
from urllib.parse import quote_plus, urlencode
from settings import *

auth_routes = Blueprint('auth_routes', __name__)

@app.route("/login")
def login():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback")
def callback():
    token = oauth.myApp.authorize_access_token()
    userinfo = token.get("userinfo")
    # Store only the user's essential information in the session
    session["user"] = {
        "access_token": token.get("access_token"),
        "id_token": token.get("id_token"),
        "refresh_token": token.get("refresh_token"),
        "username": userinfo.get("preferred_username")
    }
    return app.send_static_file('index.html')

@app.route("/logout")
def logout():
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        f'{os.getenv("KEYCLOAK_URL")}/realms/{os.getenv("KEYCLOAK_REALM")}'
        + "/protocol/openid-connect/logout?"
         + urlencode(
             {
                 "post_logout_redirect_uri": url_for("loggedOut",_external=True),
                 "id_token_hint":id_token
             },
             quote_via=quote_plus
         )
    )

@app.route("/loggedout")
def loggedOut():
    if "user" in session:
        abort(404)
    return app.send_static_file('index.html')

#when the user starts the interface asks the backend if there is an open session or not. 
#each session is individual per user
@app.route(f'{url_base}{version}user_session/',methods=['GET'])
@cross_origin()
def getUsserSession():
    if "user" in session:
        return session["user"]
    else:
        return jsonify(False)
