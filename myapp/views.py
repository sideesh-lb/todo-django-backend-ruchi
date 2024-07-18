from django.shortcuts import render

# Create your views here.
# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mongo_connection import todo_collection
from bson import ObjectId

class TodoListView(APIView):

    def get(self, request):
        todos = todo_collection.find()
        todo_list = []
        for todo in todos:
            todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
            todo_list.append(todo)
        return Response(todo_list)

    def post(self, request):
        data = request.data
        result = todo_collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return Response(data, status=status.HTTP_201_CREATED)


class TodoDetailView(APIView):

    def get(self, request, pk):
        todo = todo_collection.find_one({"_id": ObjectId(pk)})
        if todo:
            todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
            return Response(todo)
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        print("here")
        data = request.data
        data.pop('_id', None)  # Remove _id from the data if it exists
        todo_collection.update_one({"_id": ObjectId(pk)}, {"$set": data})
        updated_todo = todo_collection.find_one({"_id": ObjectId(pk)})  # Fetch the updated document
        updated_todo['_id'] = str(updated_todo['_id'])  # Convert ObjectId to string
        return Response(updated_todo, status=status.HTTP_200_OK)

    # def delete(self, request, pk):
    #     result = todo_collection.delete_one({"_id": ObjectId(pk)})
    #     print(result)
    #     if result.deleted_count:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        try:
            # Find the item before deleting it
            todo = todo_collection.find_one({"_id": ObjectId(pk)})
            
            if not todo:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Convert ObjectId to string for JSON serialization
            todo['_id'] = str(todo['_id'])

            # Delete the item from the collection
            result = todo_collection.delete_one({"_id": ObjectId(pk)})

            # Check if the item was deleted
            if result.deleted_count:
                # print(todo)
                return Response(todo, status=status.HTTP_200_OK)  # Return the deleted item
            else:
                return Response({"error": "Failed to delete todo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Internal Server Error response
        
    def patch(self, request, pk):
        try:
            data = request.data
            data.pop('_id', None)  # Remove _id from the data if it exists
            result = todo_collection.update_one({"_id": ObjectId(pk)}, {"$set": data})

            # Check if the item was updated
            if result.matched_count == 0:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

            updated_todo = todo_collection.find_one({"_id": ObjectId(pk)})  # Fetch the updated document
            updated_todo['_id'] = str(updated_todo['_id'])  # Convert ObjectId to string
            return Response(updated_todo, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)