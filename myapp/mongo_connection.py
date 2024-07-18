# myapp/mongo_connection.py

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sideesh:pavitasree@cluster-kanbas.x2jtkqg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-Kanbas')
db = client['tododb']

todo_collection = db['todonews']
