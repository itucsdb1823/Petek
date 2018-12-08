from flask_jwt_simple import get_jwt_identity, jwt_optional

from server import server
from flask_restful import Api, request, abort
from flask_cors import CORS
import server.resources as r
from server.models.User import User

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

api = Api(server)

api.add_resource(r.Register, '/api/register')
api.add_resource(r.Login, '/api/login')
api.add_resource(r.Account, '/api/account')

# -------- Lecturers ------

api.add_resource(r.GetLecturers, '/api/lecturers')
api.add_resource(r.AddLecturer, '/api/lecturers/store')
api.add_resource(r.GetLecturer, '/api/lecturers/<string:slug>')
api.add_resource(r.DeleteLecturer, '/api/lecturers/<int:lecturer_id>/delete')
api.add_resource(r.UpdateLecturer, '/api/lecturers/<int:lecturer_id>/update')

# --------- Notes -----------

api.add_resource(r.Notes, '/api/notes')
api.add_resource(r.NoteCreate, '/api/notes/store')
api.add_resource(r.NoteUpdate, '/api/notes/<int:note_id>/update')
api.add_resource(r.NoteSingle, '/api/notes/<string:note_slug>')
api.add_resource(r.NoteDelete, '/api/notes/<int:note_id>/delete')

# ------- Courses and Terms -------

api.add_resource(r.Courses, '/api/courses')
api.add_resource(r.Terms, '/api/terms')

# ------- Comments -------

api.add_resource(r.GetLecturerComments, '/api/lecturers/<int:type_id>')
api.add_resource(r.GetNoteComments, '/api/notes/<int:type_id>')
api.add_resource(r.CreateLecturerComment, '/api/lecturers/<int:type_id>/store')
api.add_resource(r.CreateNoteComment, '/api/notes/<int:type_id>/store')
api.add_resource(r.DeleteComment, '/api/comments/<int:comment_id>/delete')
api.add_resource(r.UpdateLecturerComment, '/api/lecturers/<int:type_id>/comments/<int:comment_id>/update')
api.add_resource(r.UpdateNoteComment, '/api/notes/<int:type_id>/comments/<int:comment_id>/update')

# ------ Grade Distributions ------

api.add_resource(r.AddGradeDistribution, '/api/add-grade-distribution')
api.add_resource(r.DeleteGradeDistribution, '/api/delete-grade-distribution')

# ------ Events -------

api.add_resource(r.CreateEvent, '/api/events/store')
api.add_resource(r.UpdateEvent, '/api/events/<int:event_id>/update')
api.add_resource(r.DeleteEvent, '/api/events/<int:event_id>/delete')
api.add_resource(r.GetEvent, '/api/events/<int:event_id>')
api.add_resource(r.GetEvents, '/api/events/*')

# Admin Routes
api.add_resource(r.GetAllUsers, '/admin/users')

api.add_resource(r.Test, '/api/test')


@server.before_request
@jwt_optional
def before_request():
    path = request.path.split(sep='/')
    if path[1] == 'admin':
        current_user = get_jwt_identity()
        if current_user is None or User().where('id', current_user['id']).first().hasRole('admin') is False:
            abort(401)


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    return 'Backend working yey!'
