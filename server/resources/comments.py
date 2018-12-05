from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.Comment import Comment
from server.helpers import response
from server import cur, conn

parser = reqparse.RequestParser()
parser.add_argument('comment', type=str, help='Comment must be a string')


class CreateLecturerComment(Resource):
    @jwt_required
    def post(self, type_id):
        args = parser.parse_args()
        type = 'lecturers'
        type_id = type_id
        comment = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment(_type=type, _type_id=type_id, _comment=comment, _user_id=user_id)
        result = comment.save()

        if result is False:
            return response({
                'errors': comment.getErrors()
            }, 401)

        return response({
            'message': 'Comment successfully created!'
        })


class CreateNoteComment(Resource):
    @jwt_required
    def post(self, type_id):
        args = parser.parse_args()
        type = 'notes'
        type_id = type_id
        comment = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment(_type=type, _type_id=type_id, _comment=comment, _user_id=user_id)
        result = comment.save()

        if result is False:
            return response({
                'errors': comment.getErrors()
            }, 401)

        return response({
            'message': 'Comment successfully created!'
        })


class UpdateComment(Resource):
    @jwt_required
    def post(self, comment_id):
        args = parser.parse_args()
        commentText = args['comment']
        user_id = get_jwt_identity()['id']
        comment = Comment(_id=comment_id, _user_id=user_id, _comment=commentText, _type='lecturers')
        result = comment.Update()

        if result is False:
            return response({
                'errors': comment.getErrors()
            }, 401)
        return response({
            'message': 'Comment successfully updated!'
        })


class DeleteComment(Resource):
    @jwt_required
    def post(self, comment_id):
        comment = Comment(_id=comment_id, _user_id=get_jwt_identity()['id'])
        comment.delete()

        return response({
            'message': "Comment deleted successfully"
        })


class Comments(Resource):
    def get(self, comment_id):
        comment = Comment().get(id=comment_id)

        return response({
            'Comment': comment
        })
