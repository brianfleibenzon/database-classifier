from flask import Blueprint, request, render_template, make_response
from flask_restplus import Namespace, Resource, fields
from app.controllers.database import addDatabase, startScanDatabase, getDatabase, getAllDatabases
from flask_jwt_extended import jwt_required

api = Namespace('Database')

databaseInput = api.model('Database Input', {
    'host': fields.String(required=True),
    'port': fields.Integer(required=True),
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

tables = api.model('Table', {
    'column_name': fields.String
})

schemas = api.model('Schema', {
    'table_name': fields.Nested(tables)
})

structure = api.model('Structure', {
    'schemas': fields.Nested(schemas)
})

last_scan = api.model('Last scan', {
    'history': fields.String,
    'structure': fields.Nested(structure)
})

databaseOutput = api.model('Database', {
    '_id': fields.String,
    'host': fields.String,
    'port': fields.Integer,
    'username': fields.String
})

@api.route("/scan/<string:id>/render")
@api.param('id', 'Database ID')
class DatabaseView(Resource):
    @api.response(200, 'Success')
    @api.produces(["text/html"])
    @jwt_required
    def get(self, id):
        try:
            response = getDatabase(id, ["last_scan"])
            database = response.get("last_scan")
            code = 200
        except Exception:
            database = None
            code = 404

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('database.html', id=id, database=database), code, headers)


@api.route("/scan/<string:id>")
@api.param('id', 'Database ID')
class DatabaseScan(Resource):
    @api.response(404, 'Database not found')
    @api.response(200, 'Success', last_scan)
    @jwt_required
    def get(self, id):
        try:
            response = getDatabase(id, ["last_scan"])
            return response.get("last_scan", {}), 200

        except IndexError as e:
            return {'msg': e.args[0]}, 404


    @api.response(404, 'Database not found')
    @api.response(201, 'Success')
    @jwt_required
    def post(self, id):
        try:
            response = startScanDatabase(id)
            return response, 201

        except IndexError as e:
            return {'msg': e.args[0]}, 404

        except ConnectionError as e:
            return {'msg': e.args[0]}, 502


@api.route("/")
class Database(Resource):
    @api.expect(databaseInput)
    @api.response(400, 'Parameters invalid')
    @api.response(201, 'Success', databaseOutput)
    @jwt_required
    def post(self):
        data = request.json if request.json is not None else request.form
        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')

        try:
            response = addDatabase(host, port, username, password)
            return response, 201

        except AttributeError as e:
            return {'msg': e.args[0]}, 400

    @api.response(200, 'Success', [databaseOutput])
    @jwt_required
    def get(self):
      response = getAllDatabases({'password': False, 'last_scan': False})
      return response, 200
