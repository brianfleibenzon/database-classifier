from app.helpers.database import mongo
from bson.errors import InvalidId
from datetime import datetime
from enum import Enum
import re
from app.helpers.castJson import castJson
from bson.objectid import ObjectId

def addClassifier(name, regex):
    # Validate required parameters
    if(name == "" or name is None):
        raise AttributeError("Parameter 'name' was not provided or is invalid")

    if(regex is None or type(regex) is not list):
        raise AttributeError("Parameter 'regex' was not provided or is invalid")

    if(len(regex) == 0):
        raise AttributeError("Parameter 'regex' should contain at least one element")

    # Check if there is already a classifier created with the same name
    existingClassifier = mongo.db.classifiers.find_one({"name": re.compile(name, re.IGNORECASE)})
    if (existingClassifier is None):
      insertedClassifier = mongo.db.classifiers.insert_one({"name": name, "regex": regex})
      return getClassifier(insertedClassifier.inserted_id)
    else:
      raise ValueError("There is already a classifier with the name provided")           

def getClassifier(id, fields=None):
    try:
        if(id == "" or id is None):
            raise InvalidId

        classifier = mongo.db.classifiers.find_one({"_id": ObjectId(id)}, fields)

        if(classifier is None):
            raise InvalidId

        return castJson(classifier)

    except InvalidId:
        raise IndexError("Classifier not found")

def getAllClassifiers(fields=None):
    classifiers = list(mongo.db.classifiers.find({}, fields))
    return castJson(classifiers)
