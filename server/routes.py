import sys

from flask_jwt_simple import get_jwt_identity, jwt_required, jwt_optional

from server import server, bcrypt
from flask_restful import Api, request, abort
from flask_cors import CORS
import server.resources as r
from server.helpers import response
from server.models.User import User

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

api = Api(server)

api.add_resource(r.Register, '/api/register')
api.add_resource(r.Login, '/api/login')
api.add_resource(r.Account, '/api/account')
api.add_resource(r.AddLecturer, '/api/add-lecturer')
api.add_resource(r.GetLecturer, '/api/get-lecturer/<string:slug>')
api.add_resource(r.GetLecturers, '/api/get-lecturers')
api.add_resource(r.DeleteLecturer, '/api/delete-lecturer')
api.add_resource(r.UpdateLecturer, '/api/lecturers/<int:lecturer_id>/update')
api.add_resource(r.Notes, '/api/notes')
api.add_resource(r.NoteCreate, '/api/notes/store')
api.add_resource(r.NoteUpdate, '/api/notes/<int:note_id>/update')
api.add_resource(r.NoteSingle, '/api/notes/<string:note_slug>')
api.add_resource(r.NoteDelete, '/api/notes/<int:note_id>/delete')
api.add_resource(r.Courses, '/api/courses')
api.add_resource(r.Terms, '/api/terms')

# Admin Routes
api.add_resource(r.GetAllUsers, '/admin/users')


@server.before_request
@jwt_optional
def before_request():
    path = request.path.split(sep='/')
    if path[1] == 'admin':
        current_user = get_jwt_identity()
        if current_user is None or User(_id=current_user['id']).hasRole('admin') is False:
            abort(401)


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    return 'Backend working yey!'
