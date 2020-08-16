from app.helpers.database import mongo
from flask_jwt_extended import create_access_token
from app.helpers.castJson import castJson
from app.helpers.bcrypt import encrypt, validate

def authenticate(username, password):
    # Validate required parameters
    if(username == "" or username is None):
        raise AttributeError("Parameter 'username' was not provided or is invalid")
    if(password == "" or password is None):
        raise AttributeError("Parameter 'password' was not provided or is invalid")

    # Check if the username exists and if the password match
    user = mongo.db.users.find_one({"username": username})
    if (user is not None and validate(password, user.get('password'))):
        access_token = create_access_token(identity=str(user.get('_id')))
        return {'_id': str(user.get('_id')), 'username': user.get('username'), 'token': access_token}
    else:
        raise ValueError("The username or password is not valid") 

def register(username, password):
    # Validate required parameters
    if(username == "" or username is None):
        raise AttributeError("Parameter 'username' was not provided or is invalid")
    if(password == "" or password is None):
        raise AttributeError("Parameter 'password' was not provided or is invalid")
    
    # Check if the username is already in use
    user = mongo.db.users.find_one({"username": username})
    if (user is not None):
        raise ValueError("The username is already registered")

    # Generate hash of password and register user
    inserted_user = mongo.db.users.insert_one({"username": username, "password": encrypt(password)})
    return castJson(mongo.db.users.find_one({"_id": inserted_user.inserted_id}, {"password": False}))