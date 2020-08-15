from flask import Blueprint, request
from flask_restplus import Namespace, Resource, fields
from app.controllers.classifier import addClassifier, getAllClassifiers
from flask_jwt_extended import jwt_required

api = Namespace('Classifiers')

classifierOutput = api.model('Classifier', {
    '_id': fields.String,
    'name': fields.String(required=True),
    'regex': fields.List(fields.String, required=True),
})

@api.route("/")
class Classifier(Resource):
    @api.response(200, 'Success', [classifierOutput])
    @jwt_required
    def get(self):
      response = getAllClassifiers()
      return response, 200

    @api.expect(classifierOutput)
    @api.response(400, 'Parameters invalid')
    @api.response(201, 'Success', classifierOutput)
    @jwt_required
    def post(self):
        data = request.json if request.json is not None else request.form
        name = data.get('name')
        regex = data.get('regex')

        try:
            response = addClassifier(name, regex)
            return response, 201

        except AttributeError as e:
            return {'msg': e.args[0]}, 400