from rest_framework import generics, permissions
from .models import Task
from django.contrib.auth.models import User
from .serializers import TaskSerializer, UserSerializer

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#   for filter the task by completion status
    def get_queryset(self):
        queryset = super().get_queryset()
        completed_status = self.request.query_params.get('completed')
        
        if completed_status is not None:
            if completed_status.lower() in ['true', '1']:
                queryset = queryset.filter(completed=True)
            elif completed_status.lower() in ['false', '0']:
                queryset = queryset.filter(completed=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IsOwnerOrReadOnly(permissions.BasePermission):
    #permission to allow only owners of tasks to edit or delete it.

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        #only allowed to the owner of the task.
        return obj.owner == request.user

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# for register new user 
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]