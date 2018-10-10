from flask import render_template, url_for, redirect, flash, request, abort, jsonify
from server import server#, bcrypt, db
from random import *
from flask_restful import Api
from flask_cors import CORS
from server.resources.auth import Auth

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

api = Api(server)

api.add_resource(Auth, '/api/register')


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    # user = User(first_name='Yavuzz', last_name='Kocaa', age=21)
    # user.save()
    return render_template("index.html")
