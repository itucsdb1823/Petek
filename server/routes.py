import os
import sys

from flask_jwt_simple import get_jwt_identity, jwt_optional

from server import server, send_from_directory
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
api.add_resource(r.GetUser, '/api/users/<string:slug>')
api.add_resource(r.UserUpdate, '/api/update')
api.add_resource(r.UserDelete, '/api/users/<int:user_id>/delete')

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
api.add_resource(r.DeleteGradeDistribution, '/api/delete-grade-distribution/<int:dist_id>')

# ------ Events -------

api.add_resource(r.CreateEvent, '/api/events/store')
api.add_resource(r.UpdateEvent, '/api/events/<int:event_id>/update')
api.add_resource(r.DeleteEvent, '/api/events/<int:event_id>/delete')
api.add_resource(r.GetEvent, '/api/events/<int:event_id>')
api.add_resource(r.GetEvents, '/api/events')

# Admin Routes
api.add_resource(r.GetAllUsers, '/api/admin/users')
api.add_resource(r.UserUpdateAdmin, '/api/admin/users/<int:user_id>/update')
api.add_resource(r.UserDeleteAdmin, '/api/admin/users/<int:user_id>/delete')
api.add_resource(r.LecturerDeleteAdmin, '/api/admin/lecturers/<int:lecturer_id>/delete')
api.add_resource(r.LecturerUpdateAdmin, '/api/admin/lecturers/<int:lecturer_id>/update')
api.add_resource(r.NoteDeleteAdmin, '/api/admin/notes/<int:note_id>/delete')
api.add_resource(r.NoteUpdateAdmin, '/api/admin/notes/<int:note_id>/update')
api.add_resource(r.CourseAddAdmin, '/api/admin/courses/store')
api.add_resource(r.CourseDeleteAdmin, '/api/admin/courses/<int:course_id>/delete')
api.add_resource(r.CourseUpdateAdmin, '/api/admin/courses/<int:course_id>/update')
api.add_resource(r.TermAddAdmin, '/api/admin/terms/store')
api.add_resource(r.TermDeleteAdmin, '/api/admin/terms/<int:term_id>/delete')
api.add_resource(r.TermUpdateAdmin, '/api/admin/terms/<int:term_id>/update')
api.add_resource(r.CommentDeleteAdmin, '/api/admin/comments/<int:comment_id>/delete')
api.add_resource(r.CommentUpdateAdmin, '/api/admin/comments/<int:comment_id>/update')
api.add_resource(r.EventDeleteAdmin, '/api/admin/events/<int:event_id>/delete')
api.add_resource(r.EventUpdateAdmin, '/api/admin/events/<int:event_id>/update')

api.add_resource(r.Test, '/api/test')


@server.before_request
@jwt_optional
def before_request():
    path = request.path.split(sep='/')
    if path[2] == 'admin':
        if request.method != "OPTIONS":
            current_user = get_jwt_identity()
            if current_user is None or User().where('id', current_user['id']).first().hasRole('admin') is False:
                return response({'errors': ['Please login']}, 401)


@server.route('/images/<path:path>')
def sendImage(path):
    return send_from_directory(os.path.join('../images').replace('\\', '/'), path)


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    return 'Backend working yey!'
