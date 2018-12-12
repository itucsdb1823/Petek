from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_simple import JWTManager
import psycopg2.extras
from server.config import config
from server.helpers import setEnv

server = Flask(__name__, static_url_path='')

server.config['SECRET_KEY'] = '5ea8e7ed82a4e1fd0cca8d08a003344c'
server.config['JWT_SECRET_KEY'] = 'fjsalkd131j31k3l3k1c4e1fd0cca8d08a0'
server.config['UPLOAD_FOLDER'] = 'images'
jwt = JWTManager(server)

setEnv()
params = config()

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)

# create a cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

bcrypt = Bcrypt(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from server import routes
