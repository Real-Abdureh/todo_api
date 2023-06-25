from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer


class TodoListApi(APIView):

    #checking user authentication permission
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, *args, **kwargs):

        '''
        List all the todo items for a give requested user
        '''

        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    
    def post(self, request,*args, **kwargs):

        '''
        create todo with a given todo data
        '''
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user':request.user.id

        }

        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetail(APIView):

    #permission to check if user us authenticated

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):

        '''
        Helper method to get the object with given todo_id and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        
        except Todo.DoesNotExist:
            return None
    
    #retrieve
    def get(self, request, todo_id, *args, **kwargs):

        '''
        Retrieve the Todos with given todo id
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:

            return Response(
                {"res":"object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update
    def put(self, request, todo_id, *args, **kwargs):

        '''
        updates the todos with given todo_id if exist

        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:

            return Response(
                {"res":"object with todo id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('get'),
            'user': request.user.id
        }
        serializer = TodoSerializer(instance= todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete
    def delete(self, request, todo_id, *args, **kwargs):

        '''
        Deletes the todo items with the given todo_id if exist

        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "obeject with todo does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "object delete!"},
            status=status.HTTP_200_OK
        )
    
    

    

    

# Create your views here.
