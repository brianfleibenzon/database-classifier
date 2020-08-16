from flask_pymongo import PyMongo
from app.helpers.bcrypt import encrypt

mongo = PyMongo()

def initDB():  
  mongo.db.drop_collection('users')
  mongo.db.drop_collection('history')
  mongo.db.drop_collection('databases')
  mongo.db.drop_collection('classifiers')

  mongo.db.users.insert_one({"username": 'admin', "password": encrypt('teSt@123')})
  mongo.db.classifiers.insert_one({"name": 'TEST_CLASSIFIER', "regex": ['.*test.*']})
  