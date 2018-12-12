import sys

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity

from server.models.Comment import Comment
from server.models.GradeDistribution import GradeDistribution
from server.models.Lecturer import Lecturer
from server.models.Note import Note
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
            'user': user.plus('token', user.generateToken()['jwt']).plus('admin', user.hasRole('admin')).data()
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
                'user': user.plus('token', user.generateToken()['jwt']).plus('admin', user.hasRole('admin')).data()
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


class UserDelete(Resource):
    @jwt_required
    def post(self, user_id):
        user_id = get_jwt_identity()['id']
        user = User().where('id', user_id).first()
        if user.exists() is True:
            Comment().where('user_id', user_id).get().delete()
            GradeDistribution().where('user_id', user_id).get().delete()
            Lecturer().where('user_id', user_id).get().delete()
            Note().where('user_id', user_id).get().delete()
            user.delete()
            return response({
                'message': 'User deleted with success'
            }, 200)

        return response({
            'errors': ['User could not found!']
        }, 401)


class UserUpdate(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        user_id = get_jwt_identity()['id']

        # Check if passwords are the same
        if args['password'] is not None and args['passwordConfirm'] != args['password']:
            return response({
                'errors': ['Password and Confirm Password must be same']
            }, 400)

        # Check if the email is already taken or not
        email = args['email']
        user = User().where('email', email).first()
        if user.exists() and user.ATTRIBUTES['id'] != user_id:
            return response({
                'errors': ['This email is already taken']
            }, 400)

        # Update user
        user = User().where('id', '=', user_id).first()
        if user.exists() is True:
            user.update({
                'name': args['name'],
                'email': args['email'],
                'slug': user.generateSlug(name=args['name']),
                'password': bcrypt.generate_password_hash(args['password']).decode('utf-8')
            })
            return response({
                'user': user.data()
            })

        return response({
            'errors': [
                'User could not found'
            ]
        }, 404)


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

