from server.helpers import response
from flask_restful import Resource, reqparse

from server.models.Term import Term


class Terms(Resource):
    def get(self):
        terms = Term().where().get()
        return response({
            'terms': terms.data()
        }, 200)
