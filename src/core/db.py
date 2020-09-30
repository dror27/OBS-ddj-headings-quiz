# handle db stuff

from pymongo import MongoClient
import os

def get_db():

    # open database connection
    username = db_env("DBUSER", "root")
    password=  db_env("DBPASS", "mongo")
    host = db_env("DBHOST", "mongo")
    client = MongoClient(('mongodb://%s:%s@' + host) % (username, password))
    db = client.headings
    return db

def db_env(name, defaultValue=None):
	key = "TEL_BOT_" + name
	return os.environ[key] if key in os.environ else defaultValue

def db_sources():
    return [source for source in get_db().sources.find()]

