from flask import Blueprint, request
from flask_restplus import Namespace, Resource, fields
from app.controllers.auth import authenticate, register
from flask_jwt_extended  import jwt_required

api = Namespace('Auth')

user = api.model('User', {
    '_id': fields.String,
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

authReponse = api.model('Auth Response', {
    'token': fields.String,
    '_id': fields.String,
    'username': fields.String
})

@api.route("/login")
class Auth(Resource):
    @api.expect(user)
    @api.response(402, 'Authentication credentials are not valid')
    @api.response(200, 'Success', authReponse)
    def post(self):
        data = request.json if request.json is not None else request.form
        username = data.get('username')
        password = data.get('password')

        try:
            response = authenticate(username, password)
            return response, 200

        except Exception:
            return {'msg': 'Authentication credentials are not valid'}, 402
            

@api.route("/register")
class Auth(Resource):
    @api.expect(user)
    @api.response(409, 'The username is already registered')
    @api.response(400, 'Parameters invalid')
    @api.response(201, 'Success', user)
    def post(self):
        data = request.json if request.json is not None else request.form
        username = data.get('username')
        password = data.get('password')

        try:
            response = register(username, password)
            return response, 201

        except AttributeError as e:
            return {'msg': e.args[0]}, 400

        except ValueError as e:
            return {'msg': e.args[0]}, 409