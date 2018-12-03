from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.User import User
from server.helpers import response


class GetAllUsers(Resource):
    def get(self):
        users = User().all()
        return response({
            'users': users
        })
