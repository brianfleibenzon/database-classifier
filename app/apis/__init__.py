from flask import Blueprint
from flask_restplus import Api
from .database import api as database
from .history import api as history
from .classifier import api as classifier
from .auth import api as auth

api_v1 = Blueprint("api_v1", __name__)

api = Api(api_v1, title="Database Classifier",
          description="Application for classifing databases")

api.add_namespace(database, path='/database')
api.add_namespace(history, path='/history')
api.add_namespace(classifier, path='/classifier')
api.add_namespace(auth, path='/auth')