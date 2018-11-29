from flask import render_template, url_for, redirect, flash, request, abort, jsonify
from server import server#, bcrypt, db
from random import *
from flask_restful import Api
from flask_cors import CORS
from server.resources.auth import *
from server.resources.lecturers import *
from server.resources.notes import *
from server.resources.courses import *
from server.resources.terms import *

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

api = Api(server)

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Account, '/api/account')
api.add_resource(AddLecturer, '/api/add-lecturer')
api.add_resource(GetLecturer, '/api/get-lecturer/<string:slug>')
api.add_resource(DeleteLecturer, '/api/delete-lecturer')
api.add_resource(Notes, '/api/notes')
api.add_resource(NoteCreate, '/api/notes/store')
api.add_resource(NoteUpdate, '/api/notes/update')
api.add_resource(NoteSingle, '/api/notes/<string:note_slug>')
api.add_resource(NoteDelete, '/api/notes/<int:note_id>/delete')
api.add_resource(Courses, '/api/courses')
api.add_resource(Terms, '/api/terms')


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    # user = User(first_name='Yavuzz', last_name='Kocaa', age=21)
    # user.save()
    return 'a'
