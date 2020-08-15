from flask import Blueprint, request
from flask_restplus import Namespace, Resource, fields
from app.controllers.history import getHistory, getAllHistory
from flask_jwt_extended import jwt_required

api = Namespace('History')

historyOutput = api.model('History', {
    '_id': fields.String,
    'database': fields.String,
    'started': fields.DateTime,
    'last_updated': fields.DateTime,
    'status': fields.Integer,
    'details': fields.String,
})

@api.route("/<string:id>")
@api.param('id', 'History ID')
class HistoryGetById(Resource):
    @api.response(404, 'History not found')
    @api.response(200, 'Success', historyOutput)
    @jwt_required
    def get(self, id):
        try:
            response = getHistory(id)
            return response, 200

        except IndexError as e:
            return {'msg': e.args[0]}, 404


@api.route("/")
class HistoryGetAll(Resource):
    @api.response(200, 'Success', [historyOutput])
    @jwt_required
    def get(self):
      response = getAllHistory()
      return response, 200