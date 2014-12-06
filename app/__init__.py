import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from config import basedir
from peer_server.json_server import *

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
Bootstrap(app)
users = [ 
            {"nickname":"OR1","ip":"192.168.1.168"},
            {"nickname":"OR2","ip":"192.168.1.175"}
        ]


from app import views, models

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/steris.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('steris startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Steris startup')

from flask_jsonrpc import JSONRPC
# Flask-JSONRPC
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
@jsonrpc.method('welcome')
def index():
	return 'welcome'

@jsonrpc.method('getSessionToken() -> list')
def getSessionToken():
	print "getSessionToken"
	ret = PeerServer.generate_token()
	return [ret[0], ret[1], ret[2], ret[3]]




