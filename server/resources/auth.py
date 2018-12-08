import sys

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User
from server.helpers import response
from server import bcrypt


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name must be a string')
parser.add_argument('password', type=str, help='Password must be a string')
parser.add_argument('passwordConfirm', type=str, help='Password must be a string')
parser.add_argument('email', type=str, help='Email must be a string')


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        password = args['password']
        password_confirm = args['passwordConfirm']

        if password != password_confirm:
            return response({
                'errors': [
                    'Passwords do not match'
                ]
            }, 401)

        # Rule 2
        user = User()
        user.create({
            'name': args['name'],
            'email': args['email'],
            'password': bcrypt.generate_password_hash(args['password']).decode('utf-8'),
            'slug': user.generateSlug(args['name'])
        })
        if user.validate() is False:
            return response({
                'errors': user.getErrors()
            }, 401)

        user.save()
        return response({
            'user': user.plus('token', user.generateToken()['jwt']).data()
        })


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']

        user = User().where([
            ['email', '=', email]
        ]).first()
        if user.exists() and bcrypt.check_password_hash(user.HIDDEN['password'], password):
            return response({
                'user': user.plus('token', user.generateToken()['jwt']).data()
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


class Test(Resource):
    def post(self):
        user = User().where('id', 21).first()
        user.update({
            'email': 'sa@gmail.com123',
            'name': 'Yavuz Koca'
        })

        return response({
            'user': user.data()
        })

