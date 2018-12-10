from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity

from server.models.Comment import Comment
from server.models.GradeDistribution import GradeDistribution
from server.models.Lecturer import Lecturer
from server.helpers import response
from server import cur, conn


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('password', type=str, help='Password must be a string')
parser.add_argument('passwordConfirm', type=str, help='Password must be a string')
parser.add_argument('email', type=str, help='Email must be a string')
parser.add_argument('slug', type=str, help='Slug must be a string')
parser.add_argument('user_id', type=int, help='User Id must be a string')


class AddLecturer(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        user_id = get_jwt_identity()['id']

        lecturer = Lecturer()
        lecturer.create({
            'name': name,
            'email': email,
            'slug': lecturer.generateSlug(name=name),
            'user_id': user_id
        })


        if lecturer.validate() is True:
            lecturer.save()
            return response({
                'lecturer': lecturer.data()
            }, 200)

        return response({
            'errors': lecturer.getErrors()
        }, 400)


class GetLecturer(Resource):
    def get(self, slug):
        lecturer = Lecturer().where('slug', slug).first()

        if lecturer.exists() is True:
            comments = Comment().where([['type_id', '=', lecturer.ATTRIBUTES['id']], ['type', '=', 'lecturers']])\
                .get().data()
            grade_distributions = GradeDistribution().where('lecturer_id', lecturer.ATTRIBUTES['id']).get().data()

            return response({
                'lecturer': lecturer.plus('comments', comments).plus('grade_distributions', grade_distributions).data()
            })

        return response({
            'errors': [
                'Lecturer could not found!'
            ]
        })


class GetLecturers(Resource):
    def get(self):
        lecturers = Lecturer().get()
        return response({
            'lecturers': lecturers.data()
        })


class DeleteLecturer(Resource):
    @jwt_required
    def post(self, lecturer_id):
        user_id = get_jwt_identity()['id']
        lecturer = Lecturer().where([['id', '=', lecturer_id],
                                     ['user_id', '=', user_id]]).first()
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


class UpdateLecturer(Resource):
    @jwt_required
    def post(self, lecturer_id):
        args = parser.parse_args()
        user_id = get_jwt_identity()['id']
        lecturer = Lecturer().where([['id', '=', lecturer_id],
                                     ['user_id', '=', user_id]]).first()
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


