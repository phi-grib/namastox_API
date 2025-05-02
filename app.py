# ROUTES
from manage import *
from results import *
from status import *
from notes import *
from update import *
from report import *
from keycloack import *
from flask import  url_for, session, redirect

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

    if "user" not in session:
        return redirect(url_for('login'))
        
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')

app.register_blueprint(auth_routes)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)