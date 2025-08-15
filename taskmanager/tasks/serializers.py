from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ("id", "username", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = ("id", "title", "description", "completed", "created_at", "updated_at", "owner")
        read_only_fields = ("created_at", "updated_at")
