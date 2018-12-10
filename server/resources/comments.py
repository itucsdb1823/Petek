from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.Comment import Comment
from server.models.User import User
from server.models.Lecturer import Lecturer
from server.models.Note import Note
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
        commentText = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment()
        comment.create({
            'type': type,
            'type_id': type_id,
            'comment': commentText,
            'user_id': user_id
        })

        if comment.validate() is False:
            return response({
                'errors': comment.getErrors()
            }, 401)

        user = User().where('id', user_id).first()
        comment.save()
        return response({
            'comment': comment.plus('user', user.data()).data()
        }, 200)


class CreateNoteComment(Resource):
    @jwt_required
    def post(self, type_id):
        args = parser.parse_args()
        type = 'notes'
        type_id = type_id
        commentText = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment()
        comment.create({
            'type': type,
            'type_id': type_id,
            'comment': commentText,
            'user_id': user_id
        })

        if comment.validate() is False:
            return response({
                'errors': comment.getErrors()
            }, 401)

        user = User().where('id', user_id).first()
        comment.save()
        return response({
            'comment': comment.plus('user', user.data()).data()
        }, 200)


class UpdateLecturerComment(Resource):
    @jwt_required
    def post(self, type_id, comment_id):
        args = parser.parse_args()
        commentText = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment().where([['id', '=', comment_id],
                                   ['user_id', '=', user_id]]).first()
        if comment.exists() is False or comment.validate() is False:
            return response({
                'message': 'That comment does not exist or it does not belong to you'
            }, 401)
        comment.update({
            'comment': commentText,
        })
        return response({
            'message': 'Comment successfully updated!'
        }, 200)


class UpdateNoteComment(Resource):
    @jwt_required
    def post(self, type_id, comment_id):
        args = parser.parse_args()
        commentText = args['comment']
        user_id = get_jwt_identity()['id']

        comment = Comment().where([['id', '=', comment_id],
                                   ['user_id', '=', user_id]]).first()
        if comment.exists() is False or comment.validate() is False:
            return response({
                'message': 'That comment does not exist or it does not belong to you'
            }, 401)
        comment.update({
            'comment': commentText,
        })
        return response({
            'message': 'Comment successfully updated!'
        }, 200)


class DeleteComment(Resource):
    @jwt_required
    def post(self, comment_id):
        user_id = get_jwt_identity()['id']
        comment = Comment().where([['id', '=', comment_id],
                                   ['user_id', '=', user_id]]).first()
        if comment.exists():
            comment.delete()
            return response({
                'message': 'Comment deleted successfully'
            }, 202)
        return response({
            'message': 'Comment not found in the database'
        }, 404)


#class GetComment(Resource):
#    def get(self, comment_id):
#        comment = Comment().where('id', comment_id).first()
#        user = User().where('id', comment.ATTRIBUTES['user_id']).first()
#
#        return response({
#            'Comment': comment.plus('user', user).data()
#        })


class GetLecturerComments(Resource):
    def get(self, type_id):
        comments = Comment().where([['type', '=', 'lecturers'],
                        ['type_id', '=', type_id]]).orderBy().get().data()
        for comment in comments:
            user = User().where('id', comment['user_id']).first()
            comment['user'] = {
                'id': user.ATTRIBUTES['id']
            }

        return response({
            'comments': comments
        }, 200)


class GetNoteComments(Resource):
    def get(self, type_id):
        comments = Comment().where([['type', '=', 'notes'],
                        ['type_id', '=', type_id]]).orderBy().get().data()
        for comment in comments:
            user = User().where('id', comment['user_id']).first()
            comment['user'] = user.data()

        return response({
            'comments': comments
        }, 200)
