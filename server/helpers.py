from flask import make_response, jsonify


def response(json, status=200):
    resp = make_response(jsonify(json), status)
    resp.headers['content-type'] = 'application/json'
    return resp
