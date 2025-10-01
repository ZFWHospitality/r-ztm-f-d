from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Task_Manager_API.models import Task
from Task_Manager_API.serializers import TaskSerializer
from numpy import random

@api_view()
def view_dtl(request):
    return Response({'success': 409, 'message': 'api'})

@api_view(['GET', 'POST'])
def view_Task(request):
    # GET method to retrieve all Tasks
    if request.method == 'GET':
        Task_obj = Task.objects.all()
        paginator = Paginator(Task_obj, 10)  # Show 10 tasks per page
        try:
            page = request.GET['page']
        except Exception as e:
            page = 1
        Task_obj = paginator.get_page(page)
        serializer = TaskSerializer(Task_obj, many=True)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # POST method to create a new Task
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Task created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT','DELETE'])
def TaskByID(request,pk):
    # GET method to retrieve all Tasks
    if request.method == 'GET':
        Task_obj = Task.objects.get(pk=pk)
        serializer = TaskSerializer(Task_obj, many=False)
        return Response({'msg': 'Successfully retrieved data', 'data': serializer.data}, status=status.HTTP_200_OK)

    # PUT method to update a Task (full update)
    elif request.method == 'PUT':
        Task_obj = Task.objects.get(pk=pk)
        serializer = TaskSerializer(Task_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Task updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a Task
    elif request.method == 'DELETE':
        Task_obj = Task.objects.get(pk=pk)
        Task_obj.delete()
        return Response({'msg': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'msg': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)