from flask import render_template, url_for, redirect, flash, request, abort, jsonify
from server import server#, bcrypt, db
from random import *
from flask_restful import Api
from flask_cors import CORS
from server.resources.auth import *

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

api = Api(server)

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Account, '/api/account')


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    # user = User(first_name='Yavuzz', last_name='Kocaa', age=21)
    # user.save()
    return 'a'
