from app.helpers.database import mongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from enum import Enum
from app.helpers.castJson import castJson

class ExecutionStatus(Enum):
  ERROR = -1
  RUNNING = 0
  SUCCESS = 1


def addHistory(databaseId, status=ExecutionStatus.RUNNING):
    try:
        insertedHistory = mongo.db.history.insert_one({"started": datetime.utcnow(), "database": ObjectId(databaseId), "status": status.value, "details": ""})
        
        return getHistory(insertedHistory.inserted_id)

    except InvalidId:
        raise IndexError("Invalid database ID")


def updateHistory(id, status, details=""):
    try:
        if(id == "" or id is None):
            raise InvalidId

        mongo.db.history.update_one({"_id": ObjectId(id)}, {"$set": {"last_updated": datetime.utcnow(), "status": status.value, "details": details}})
        
        return getHistory(id)

    except InvalidId:
        raise IndexError("History not found")

def getHistory(id, fields = None):
    try:
        if(id == "" or id is None):
            raise InvalidId

        history = mongo.db.history.find_one({"_id": ObjectId(id)}, fields)

        if(history is None):
            raise InvalidId

        return castJson(history)

    except InvalidId:
        raise IndexError("History not found")


def getAllHistory(fields = None):
    history = list(mongo.db.history.find({}, fields))

    return castJson(history)
