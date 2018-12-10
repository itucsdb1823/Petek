from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity

from server.models.Comment import Comment
from server.models.Note import Note
from server.models.User import User
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

        note = Note()
        note.create({
            'title': title,
            'content': content,
            'lecturer': lecturer,
            'link': link,
            'course_id': course_id,
            'course_code': course_code,
            'english': english,
            'term_id': term_id,
            'user_id': user_id,
            'slug': note.generateSlug(name=title)
        })

        if note.validate() is False:
            return response({
                'errors': note.getErrors()
            }, 401)

        user = User().where('id', user_id).first()
        note.save()
        return response({
            'note': note.plus('user', user.data()).data()
        }, 200)


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

        note = Note().where([['id', '=', note_id],
                                   ['user_id', '=', user_id]]).first()

        if note.exists() is False or note.validate() is False:
            return response({
                'message': 'That note does not exist or it does not belong to you'
            }, 401)

        note.update({
            'title': title,
            'content': content,
            'lecturer': lecturer,
            'link': link,
            'course_id': course_id,
            'course_code': course_code,
            'english': english,
            'term_id': term_id,
            'slug': note.generateSlug(name=title)
        })
        return response({
            'message': 'Note successfully updated!'
        }, 200)


class NoteDelete(Resource):
    @jwt_required
    def post(self, note_id):
        user_id = get_jwt_identity()['id']
        note = Note().where([['id', '=', note_id],
                               ['user_id', '=', user_id]]).first()

        if note.exists():
            note.delete()
            return response({
                'message': 'Note deleted successfully'
            }, 202)
        return response({
            'message': 'Note does not exist or it is not yours to delete'
        }, 404)


class NoteSingle(Resource):
    def get(self, note_slug):
        note = Note().where('slug', note_slug).first().data()
        user = User().where('id', note['user_id']).first()
        note['user'] = user.data()
        comments = Comment().where([['type', '=', 'notes'], ['type_id', '=', note['id']]]).get()
        note['comments'] = comments.data()
        return response({
            'notes': note
        }, 200)


class Notes(Resource):
    def get(self):
        notes = Note().where().orderBy().get().data()
        for note in notes:
            user = User().where('id', note['user_id']).first()
            note['user'] = user.data()

        return response({
            'notes': notes
        }, 200)
