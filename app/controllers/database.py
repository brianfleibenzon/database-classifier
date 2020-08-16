from app.helpers.database import mongo
from app.helpers.crypto import encrypt, decrypt
from bson.objectid import ObjectId
from bson.errors import InvalidId
import mysql.connector
from threading import Thread
import re
from app.controllers.history import addHistory, updateHistory, ExecutionStatus
from app.controllers.classifier import getAllClassifiers
from app.helpers.castJson import castJson


def addDatabase(host, port, username, password):
    # Validate required parameters
    if(host == "" or host is None):
        raise AttributeError("Parameter 'host' was not provided or is invalid")
    if(port == "" or port is None):
        raise AttributeError("Parameter 'port' was not provided or is invalid")
    if(username == "" or username is None):
        raise AttributeError("Parameter 'username' was not provided or is invalid")
    if(password == "" or password is None):
        raise AttributeError("Parameter 'password' was not provided or is invalid")

    try:
        int_port = int(port)        

        database_id = mongo.db.databases.insert_one({"host": host, "port": int_port, "username": username, "password": encrypt(password)})

        return getDatabase(database_id.inserted_id, {'password': False})

    except ValueError:
        raise AttributeError("Parameter 'port' is not a valid integer")


def startScanDatabase(id):    
    # Get database connection details
    database = getDatabase(id)
    
    # Add a history record
    history = addHistory(id)

    try:
        # Try connecting to MySQL Server, so as in case of failure the error is retrieved synchronously
        mysqldb = mysql.connector.connect(
            host=database.get("host"),
            port=database.get("port"),
            user=database.get("username"),
            password=decrypt(database.get("password"))
        )
        
        # Start the scanning process in a new thread
        thread = Thread(target=scanDatabase, args=(id, history.get("_id"), mysqldb))
        thread.daemon = True
        thread.start()

        return history

    except mysql.connector.Error as err:                
        # Update history record with the error received and output the message
        updateHistory(history.get("_id"), ExecutionStatus.ERROR, err.args)
        raise ConnectionError(err.args)


def scanDatabase(id, historyId, mysqldb):
    cursor = mysqldb.cursor()

    # Execute MySQL query for getting all the schemas, tables and columns without including system ones
    cursor.execute("SELECT `TABLE_SCHEMA`, `TABLE_NAME`, `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` NOT IN ('information_schema', 'performance_schema', 'sys', 'mysql')")

    columns = list(cursor.fetchall())

    columns_parsed = {}

    # Retrieve all defined classifiers
    classifiers = list(getAllClassifiers())

    # Iterate over all columns of each table of each schema
    for (table_schema, table_name, column_name) in columns:
        matches = list()        
        # Iterate over all the classifier types
        for classifier in classifiers:            
            # Join all the classifiers of a particular tpe to make just one comparison
            temp = '(?:%s)' % '|'.join(classifier.get("regex"))
            
            # Check if the regex match with the column name ignoring the case
            if re.match(temp, column_name, re.IGNORECASE):                
                # As it matched, add it to matches list, as multiple matches can be found for a specific column
                matches.append(classifier.get("name"))

        # Save the result in a hashtable
        columns_parsed.setdefault(table_schema, {}).setdefault(
            table_name, {})[column_name] = matches

    # Update the database record with the last scan structure
    mongo.db.databases.update_one({'_id': ObjectId(id)}, {'$set': {'last_scan': {'history': ObjectId(historyId), 'structure': columns_parsed}}})

    # Update history record status
    updateHistory(historyId, ExecutionStatus.SUCCESS)

    cursor.close()
    mysqldb.close()

def getDatabase(id, fields = None):
    try:
        if(id == "" or id is None):
            raise InvalidId

        database = mongo.db.databases.find_one({"_id": ObjectId(id)}, fields)

        if(database is None):
            raise InvalidId
        
        return castJson(database)

    except InvalidId:
        raise IndexError("Database not found")

def getAllDatabases(fields = None):
    databases = list(mongo.db.databases.find({}, fields))

    return castJson(databases)

