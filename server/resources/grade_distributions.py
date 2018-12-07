import base64
import os
import re
from PIL import Image
from io import BytesIO

import werkzeug

from server import server
from server.helpers import response
from flask_restful import Resource, reqparse
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity

from server.models.GradeDistribution import GradeDistribution
import sys

parser = reqparse.RequestParser()
parser.add_argument('term_id', type=int, help='Term must be a int')
parser.add_argument('course_id', type=int, help='Course must be a int')
parser.add_argument('english', type=bool, help='English must be a boolean')
parser.add_argument('course_code', type=int, help='Course Code must be a int')
parser.add_argument('lecturer_id', type=int, help='Lecturer must be a int')
parser.add_argument('image', type=str, help='image must be a string')
parser.add_argument('id', type=int, help='id must be a file')


def convert_and_save(b64_string, filename):
    with open(filename, "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))


class AddGradeDistribution(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        grade_distribution = GradeDistribution(
            lecturer_id=args['lecturer_id'],
            user_id=get_jwt_identity()['id'],
            term_id=args['term_id'],
            course_id=args['course_id'],
            course_code=args['course_code'],
            english=args['english'],
        )

        file = args['image']

        if file:
            filename = grade_distribution.image = grade_distribution.generateImageName()
            imgdata = base64.b64decode(file)

            with open(server.config['UPLOAD_FOLDER'] + '/' + filename, 'wb') as f:
                f.write(imgdata)

            file_size = os.stat(os.path.join(server.config['UPLOAD_FOLDER'], filename)).st_size
            print('393343', file=sys.stderr)
            if file_size > 5000000:
                os.remove(os.path.join(server.config['UPLOAD_FOLDER'], filename))
                return response({
                    'errors': [
                        'File size must be lower than 5 MB'
                    ]
                })

            if grade_distribution.save() is True:
                return response({
                    'message': 'Grade distribution saved successfully'
                })

            return response({
                'errors': grade_distribution.getErrors()
            }, 400)

        return response({
            'errors': [
                'File could not found!'
            ],
            'file': file
        }, 400)


class DeleteGradeDistribution(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        grade_distribution = GradeDistribution(
            _id=args['id'],
            user_id=get_jwt_identity()['id'],
        )
        grade_distribution.delete()

        return response({
            'message': 'Grade Distribution has deleted successfully'
        })
