from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["completed"]               # /api/tasks/?completed=true
    search_fields = ["title", "description"]       # /api/tasks/?search=report
    ordering_fields = ["created_at", "updated_at"] # /api/tasks/?ordering=created_at

    def get_queryset(self):
        # Regular users: only see their own tasks; admins see all
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(owner=user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        qs = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

# Create your views here.
