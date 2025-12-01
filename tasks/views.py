from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

task_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'owner': openapi.Schema(type=openapi.TYPE_STRING),
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'description': openapi.Schema(type=openapi.TYPE_STRING),
        'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    }
)

update_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'task': task_schema
    }
)

delete_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING)
    }
)

task_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['title'],
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, example='Buy groceries'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, example='Milk, eggs, bread'),
        'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
    },
)

paginated_task_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
        'next': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
        'previous': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True),
        'results': openapi.Schema(type=openapi.TYPE_ARRAY, items=task_schema)
    }
)

class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD for Task model.
    - Only authenticated users can create tasks.
    - Owners (or staff) can update/delete their tasks.
    - List returns only tasks owned by the requesting user (unless staff).
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'owner__username']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Task.objects.all().order_by('-created_at')
            return Task.objects.filter(owner=user).order_by('-created_at')
        return Task.objects.none()


    @swagger_auto_schema(
        request_body=task_request_body,
        responses={201: task_schema}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new task. Owner is set to the authenticated user.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: paginated_task_list_schema})
    def list(self, request, *args, **kwargs):
        """
        List tasks. For regular users returns only their tasks; for staff returns all tasks.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: task_schema})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=task_request_body,
        responses={200: update_response_schema}
    )
    def update(self, request, *args, **kwargs):
        """
        Full update (PUT). Returns a message and the updated task.
        """
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Task updated successfully!",
            "task": response.data
        }
        return response

    @swagger_auto_schema(
        request_body=task_request_body,
        responses={200: update_response_schema}
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update (PATCH). Returns a message and the updated task.
        """
        response = super().partial_update(request, *args, **kwargs)
        response.data = {
            "message": "Task updated successfully!",
            "task": response.data
        }
        return response

    @swagger_auto_schema(
        responses={200: delete_response_schema}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a task. Returns a success message with task title.
        """
        instance = self.get_object()
        title = instance.title
        self.perform_destroy(instance)
        return Response(
            {"message": f"Task '{title}' has been deleted successfully."},
            status=status.HTTP_200_OK
        )


class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Basic user create/list viewset. Only POST and GET are allowed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'get']
