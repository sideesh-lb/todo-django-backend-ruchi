# myapp/mongo_connection.py

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['tododb']

# Example collection
todo_collection = db['todonews']
