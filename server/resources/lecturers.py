from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
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

        lecturer = Lecturer(name, email, user_id)
        result = lecturer.create()
        if result is False:
            return response({
                'errors': [
                    "There is already a lecturer with this email"
                ]
            }, 400)
        return result


class GetLecturer(Resource):
    def get(self, slug):
        lecturer = Lecturer().get(slug)
        return response({
            'lecturer': lecturer
        })


class GetLecturers(Resource):
    def get(self):
        lecturers = Lecturer().all()
        return response({
            'lecturers': lecturers
        })


class DeleteLecturer(Resource):
    def post(self):
        args = parser.parse_args()
        slug = args['slug']
        user_id = args['user_id']
        print(slug)
        print(user_id)
        Lecturer().delete(slug=slug, user_id=user_id)


