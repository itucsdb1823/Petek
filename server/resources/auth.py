from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User
from server.helpers import response


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('password', type=str, help='Password must be a string')
parser.add_argument('passwordConfirm', type=str, help='Password must be a string')
parser.add_argument('email', type=str, help='Email must be a string')


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        password = args['password']
        password_confirm = args['passwordConfirm']
        email = args['email']

        # Validation rules start

        # Rule 1
        if password != password_confirm:
            return response({
                'errors': [
                    'Passwords do not match'
                ]
            }, 401)

        # Rule 2
        user = User(name, password, email)
        if user.is_valid() is False:
            return response({
                'errors': [
                    'This email has taken'
                ]
            }, 401)

        # Validation rules end
        token = user.create()

        return response({
            'name': user.name,
            'email': user.email,
            'slug': user.slug,
            'id': user.id,
            'token': token
        })


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']

        user = User.get(email, password)

        if user is not None:
            token = {'jwt': create_jwt(identity={
                'id': user['id']
            })}
            return response({
                'name': user['name'],
                'email': user['email'],
                'token': token['jwt'],
                'id': user['id'],
                'slug': user['slug']
            })

        return response({
            'errors': [
                'Credentials do not match with our records.'
            ]
        }, 401)


class Account(Resource):
    @jwt_required
    def get(self):
        return jsonify({
            'user': get_jwt_identity()
        })
