from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.Note import Note
from server.helpers import response
from server import cur, conn

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title must be a string')
parser.add_argument('content', type=str, help='Content must be a string')
parser.add_argument('lecturer', type=str, help='Lecturer must be a string')
parser.add_argument('link', type=str, help='Link must be a string')
parser.add_argument('course_id', type=int, help='Course Id must be a int')
parser.add_argument('course_code', type=int, help='Course Code must be a int')
parser.add_argument('english', type=bool, help='English must be a boolean')
parser.add_argument('term_id', type=int, help='Term Id must be a int')


class NoteCreate(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        title = args['title']
        content = args['content']
        lecturer = args['lecturer']
        link = args['link']
        course_id = args['course_id']
        course_code = args['course_code']
        english = args['english']
        term_id = args['term_id']
        user_id = get_jwt_identity()['id']

        note = Note(title=title, content=content,
                    lecturer=lecturer, link=link, course_id=course_id, course_code=course_code,
                    english=english, term_id=term_id, user_id=user_id)

        if note.save() is False:
            return response({
                'errors': note.getErrors()
            }, 401)

        return response({
            'message': 'Note successfully created!'
        })


class NoteUpdate(Resource):
    @jwt_required
    def post(self, note_id):
        args = parser.parse_args()
        title = args['title']
        content = args['content']
        lecturer = args['lecturer']
        link = args['link']
        course_id = args['course_id']
        course_code = args['course_code']
        english = args['english']
        term_id = args['term_id']
        user_id = get_jwt_identity()['id']

        new_note = Note(title=title, content=content,
                        lecturer=lecturer, link=link, course_id=course_id, course_code=course_code,
                        english=english, term_id=term_id, user_id=user_id, _id=note_id
                        )

        if new_note.update():
            return response({
                'message': 'Note successfully updated!'
            })
        else:
            return response({
                'errors': new_note.getErrors()
            }, 401)


class NoteDelete(Resource):
    @jwt_required
    def post(self, note_id):
        note = Note(_id=note_id, user_id=get_jwt_identity()['id'])
        note.delete()

        return response({
            'message': "Note deleted successfully"
        })


class Notes(Resource):
    def get(self):
        notes = Note().all()

        return response({
            'notes': notes
        })


class NoteSingle(Resource):
    def get(self, note_slug):
        note = Note().get(slug=note_slug)

        return response({
            'note': note
        })
