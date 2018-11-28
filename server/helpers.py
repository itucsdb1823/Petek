import os

from flask import make_response, jsonify


def response(json, status=200):
    resp = make_response(jsonify(json), status)
    resp.headers['content-type'] = 'application/json'
    return resp


def setEnv():
    if os.environ.get('DATABASE', None) is not None:
        print('Printing environment variables')
        f = open('server/database.ini', 'w')
        f.write("[postgresql]")
        f.write("\nuser=" + str(os.environ.get('USER')))
        f.write("\nhost=" + str(os.environ.get('HOST')))
        f.write("\npassword=" + str(os.environ.get('PASSWORD')))
        f.write("\ndatabase=" + str(os.environ.get('DATABASE')))
        f.close()
        j = open('frontend/config.js', 'w')
        j.write('export const baseURL = \'https://dummy-server-08.herokuapp.com/api\';')
        j.close()
