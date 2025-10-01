from rest_framework import serializers
from Task_Manager_API.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'