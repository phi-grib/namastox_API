# ROUTES
from manage import *
from results import *
from status import *
from notes import *
from update import *
from report import *
from keycloack import *
from flask import Flask, render_template, url_for, session, abort, redirect
from urllib.parse import quote_plus, urlencode
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')

app.register_blueprint(auth_routes)
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)