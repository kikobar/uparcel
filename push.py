from pymongo import MongoClient
from config import *
import sys
import json

def push(document):
	client = MongoClient(CONNECTION_STRING)
	database = client[DATABASE]
	collection = database[COLLECTION]
	collection.insert_one(document)
	
	
if __name__ == '__main__':
    push(json.loads(sys.argv[1]))
    
