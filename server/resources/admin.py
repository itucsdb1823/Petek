from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User
from server.models.Lecturer import Lecturer
from server.models.Note import Note
from server.models.Course import Course
from server.models.Term import Term
from server.models.Comment import Comment
from server.models.Event import Event
from server.helpers import response

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('comment', type=str, help='Comment must be a string')
parser.add_argument('title', type=str, help='Title must be a string')
parser.add_argument('description', type=str, help='Description must be a string')
parser.add_argument('started_at', type=str, help='Started at must be a string')
parser.add_argument('max_participant', type=int, help='Max participant must be a number')
parser.add_argument('password', type=str, help='Password must be a string')
parser.add_argument('passwordConfirm', type=str, help='Password must be a string')
parser.add_argument('email', type=str, help='Email must be a string')
parser.add_argument('slug', type=str, help='Slug must be a string')
parser.add_argument('season', type=str, help='Season must be a string')
parser.add_argument('term_year', type=str, help='Term year must be a string')
parser.add_argument('user_id', type=int, help='User Id must be a number')
parser.add_argument('course_id', type=int, help='Course Id must be a number')
parser.add_argument('term_id', type=int, help='Term Id must be a number')
parser.add_argument('english', type=bool, help='English must be a boolean')
parser.add_argument('course_code', type=int, help='Course Code must be an int')
parser.add_argument('content', type=str, help='Content must be a string')
parser.add_argument('lecturer', type=str, help='Lecturer must be a string')
parser.add_argument('link', type=str, help='Link must be a string')


class GetAllUsers(Resource):
    def get(self):
        users = User().where().orderBy().get()
        return response({
            'users': users.data()
        })


class LecturerDeleteAdmin(Resource):
    @jwt_required
    def post(self, lecturer_id):
        lecturer = Lecturer().where('id', lecturer_id).first()
        if lecturer.exists() is True:
            lecturer.delete()
            return response({
                'message': 'Lecturer deleted'
            })

        return response({
            'errors': [
                'Lecturer could not found'
            ]
        }, 401)


class LecturerUpdateAdmin(Resource):
    def post(self, lecturer_id):
        args = parser.parse_args()
        lecturer = Lecturer().where('id', '=', lecturer_id).first()
        if lecturer.exists() is True:
            lecturer.update({
                'name': args['name'],
                'email': args['email'],
                'slug': lecturer.generateSlug(name=args['name'])
            })
            return response({
                'lecturer': lecturer.data()
            })

        return response({
            'errors': [
                'Lecturer could not found'
            ]
        }, 404)


class NoteDeleteAdmin(Resource):
    @jwt_required
    def post(self, note_id):
        note = Note().where('id', '=', note_id).first()

        if note.exists():
            note.delete()
            return response({
                'message': 'Note deleted successfully'
            }, 202)
        return response({
            'message': 'Note does not exist'
        }, 404)


class NoteUpdateAdmin(Resource):
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

        note = Note().where('id', '=', note_id).first()

        if note.exists() is False:
            return response({
                'message': 'That note does not exist'
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


class CourseAddAdmin(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        name = args['name']

        course = Course()
        course.create({
            'name': name,
        })

        if course.validate() is True:
            course.save()
            return response({
                'course': course.data()
            }, 200)

        return response({
            'errors': course.getErrors()
        }, 400)


class CourseDeleteAdmin(Resource):
    @jwt_required
    def post(self, course_id):
        course = Course().where('id', '=', course_id).first()

        if course.exists():
            course.delete()
            return response({
                'message': 'Course deleted successfully'
            }, 202)
        return response({
            'message': 'Course does not exist'
        }, 404)


class TermAddAdmin(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        season = args['season']
        term_year = args['term_year']

        term = Term()
        term.create({
            'season': season,
            'term_year': term_year
        })

        if term.validate() is True:
            term.save()
            return response({
                'course': term.data()
            }, 200)

        return response({
            'errors': term.getErrors()
        }, 400)


class TermDeleteAdmin(Resource):
    @jwt_required
    def post(self, term_id):
        term = Term().where('id', '=', term_id).first()

        if term.exists():
            term.delete()
            return response({
                'message': 'Term deleted successfully'
            }, 202)
        return response({
            'message': 'Term does not exist'
        }, 404)


class CommentDeleteAdmin(Resource):
    @jwt_required
    def post(self, comment_id):
        comment = Comment().where('id', '=', comment_id).first()
        if comment.exists():
            comment.delete()
            return response({
                'message': 'Comment deleted successfully'
            }, 202)
        return response({
            'message': 'Comment not found in the database'
        }, 404)


class CommentUpdateAdmin(Resource):
    @jwt_required
    def post(self, comment_id):
        args = parser.parse_args()
        commentText = args['comment']

        comment = Comment().where('id', '=', comment_id).first()
        if comment.exists() is False:
            return response({
                'message': 'That comment does not exist'
            }, 401)
        comment.update({
            'comment': commentText,
        })
        return response({
            'message': 'Comment successfully updated!'
        }, 200)


class EventDeleteAdmin(Resource):
    @jwt_required
    def post(self, event_id):
        event = Event().where('id', '=', event_id).first()
        if event.exists():
            event.delete()
            return response({
                'message': 'Event deleted successfully'
            }, 202)
        return response({
            'message': 'Event does not exist'
        }, 404)


class EventUpdateAdmin(Resource):
    @jwt_required
    def post(self, event_id):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']

        event = Event().where('id', '=', event_id).first()

        if event.exists() is False:
            return response({
                'message': 'That event does not exist'
            }, 401)
        event.update({
            'title': title,
            'description': description,
            'max_participant': max_participant,
            'started_at': started_at
        })
        return response({
            'message': 'Event successfully updated!'
        }, 200)
