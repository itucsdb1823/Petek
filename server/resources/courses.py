from server.helpers import response
from flask_restful import Resource, reqparse

from server.models.Course import Course


class Courses(Resource):
    def get(self):
        courses = Course().all()

        return response({
            'courses': courses
        })
