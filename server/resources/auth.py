from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('password', type=str, help='Password must be a string')


class Register(Resource):
    def get(self):
        return jsonify({
            'sa': 'as'
        })


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        name = args['name']
        password = args['password']

        user = User.get(name, password)

        if user is not None:
            token = {'jwt': create_jwt(identity={
                'name': user['name'],
                'email': user['email'],
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
