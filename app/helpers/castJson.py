import json
from bson.objectid import ObjectId
from datetime import datetime

class JSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
      return str(o)
    if isinstance(o, datetime):
      return o.isoformat()
    return json.JSONEncoder.default(self, o)

# Parse JSON to cast ObjectId and datetime to string
def castJson(data):
  return json.loads(json.dumps(data, cls=JSONEncoder))