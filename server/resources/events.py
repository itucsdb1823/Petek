from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from server.models.Event import Event
from server.helpers import response
from server import cur, conn
from server.models.User import User

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title must be a string')
parser.add_argument('description', type=str, help='Description must be a string')
parser.add_argument('max_participant', type=int, help='Max participant must be a number')
parser.add_argument('started_at', type=str, help='Start date must be a string')


class CreateEvent(Resource):
    @jwt_required
    def post(self):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']
        user_id = get_jwt_identity()['id']

        event = Event()
        event.create({
            'title': title,
            'description': description,
            'max_participant': max_participant,
            'started_at': started_at,
            'user_id': user_id
        })

        if event.validate() is False:
            return response({
                'errors': event.getErrors()
            }, 401)

        user = User().where('id', user_id).first()
        event.save()
        return response({
            'event': event.plus('user', user.data()).data()
        }, 200)


class UpdateEvent(Resource):
    @jwt_required
    def post(self, event_id):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        max_participant = args['max_participant']
        started_at = args['started_at']
        user_id = get_jwt_identity()['id']

        event = Event().where([['id', '=', event_id],
                                   ['user_id', '=', user_id]]).first()

        if event.exists() is False or event.validate() is False:
            return response({
                'message': 'That event does not exist or it does not belong to you'
            }, 401)
        event.update({
            'title': title,
            'description': description,
            'max_participant': max_participant,
            'started_at': started_at
        })
        return response({
            'message': 'Event successfully updated!'
        }, 200)


class DeleteEvent(Resource):
    @jwt_required
    def post(self, event_id):
        user_id = get_jwt_identity()['id']
        event = Event().where([['id', '=', event_id],
                                   ['user_id', '=', user_id]]).first()
        if event.exists():
            event.delete()
            return response({
                'message': 'Event deleted successfully'
            }, 202)
        return response({
            'message': 'Event does not exist or it is not yours to delete'
        }, 404)


class GetEvent(Resource):
    def get(self, event_id):
        event = Event().where('id', event_id).first().data()
        user = User().where('id', event['user_id']).first()
        event['user'] = user.data()
        return response({
            'event': event
        }, 200)


class GetEvents(Resource):
    def get(self):
        events = Event().where().orderBy().get().data()
        for event in events:
            user = User().where('id', event['user_id']).first()
            event['user'] = user.data()

        return response({
            'events': events
        }, 200)
