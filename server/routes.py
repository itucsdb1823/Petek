from server import server
from flask_restful import Api
from flask_cors import CORS
import server.resources as r

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


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    return 'Backend working yey!'
