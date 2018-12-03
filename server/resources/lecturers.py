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
        return response({
            'lecturer': lecturer.name
        })

class GetLecturer(Resource):
    def get(self, lecturer_slug):
        lecturer = Lecturer().get(slug=lecturer_slug)
        return response({
            'lecturer': lecturer
        })

class DeleteLecturer(Resource):
    @jwt_required
    def post(self, lecturer_id):
        user_id = get_jwt_identity()['id']
        print(lecturer_id)
        print(user_id)
        lect = Lecturer()
        result = lect.delete(lecturer_id=lecturer_id, user_id=user_id)
        if result is False:
            return response({
                'errors': lect.GetErrors()
            })
        return response({
            "Success: Lecturer deleted"
        })

class UpdateLecturer(Resource):
    @jwt_required
    def post(self, lecturer_id):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        user_id = get_jwt_identity()['id']
        lecturer = Lecturer(name=name, email=email, user_id=user_id)
        lecturer.id = lecturer_id
        result = lecturer.update()
        if result is False:
            return response({
                'errors': lecturer.GetErrors()
            })
        return response({
            'lecturer': lecturer
        })


