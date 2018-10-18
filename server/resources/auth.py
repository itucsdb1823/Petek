from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User
from server import cur, conn


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('password', type=str, help='Password must be a string')
parser.add_argument('password_confirm', type=str, help='Password must be a string')
parser.add_argument('email', type=str, help='Email must be a string')


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        password = args['password']
        password_confirm = args['password_confirm']
        email = args['email']

        # Validation rules start

        # Rule 1
        if(password != password_confirm):
            print("Passwords do not match")
            return False

        # Rule 2
        user = User(name, password, email)
        if user.is_valid() is False:
            print("User is not valid")
            return False

        # Validation rules end
        token = user.create()

        return jsonify({
            'access_token': token,
            'data': {
                'name': name,
                'email': email
            }
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
            return jsonify({
                'access_token': token,
                'data': {
                    'name': user['name'],
                    'email': user['email'],
                }
            })

        return jsonify({
            'data': 'Credentials do not match with our records.'
        }, 401)


class Account(Resource):
    @jwt_required
    def get(self):
        return jsonify({
            'user': get_jwt_identity()
        })
