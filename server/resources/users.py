from server.helpers import response
from flask_restful import Resource

from server.models.User import User


class GetUser(Resource):
    def get(self, slug):
        user = User().where('slug', slug).first()
        if user.exists() is True:
            return response({
                'user': user.data()
            })

        return response({
            'errors': ['User could not found']
        })