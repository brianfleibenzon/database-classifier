from flask import Flask
from flask_cors import CORS
from app.apis import api_v1, api
from app.helpers.database import mongo
from flask_jwt_extended import JWTManager
import os

def create_app(testConfig=None):
    app = Flask(__name__)
    CORS(app)

    # Verify all required ENV variables
    if(testConfig is None):
        if(os.environ.get("MONGO_URI") is None):
            raise Exception("MONGO_URI environment variable is not defined")

        if(os.environ.get("CRYPTO_KEY") is None):
            raise Exception("CRYPTO_KEY environment variable is not defined")

        if(os.environ.get("JWT_KEY") is None):
            raise Exception("JWT_KEY environment variable is not defined")

        
        app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
        app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_KEY")
        app.config['CRYPTO_KEY'] = os.environ.get("CRYPTO_KEY")
    else:
        app.config["MONGO_URI"] = testConfig.get("MONGO_URI")
        app.config['JWT_SECRET_KEY'] = testConfig.get("JWT_KEY")
        app.config['CRYPTO_KEY'] = testConfig.get("CRYPTO_KEY")
    
    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    # Initialize JWT
    jwt = JWTManager(app)    
    jwt._set_error_handler_callbacks(api)

    # Initialize MongoDB conneciton 
    mongo.init_app(app)

    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app
