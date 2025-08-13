from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        #tasks shorted by created_at
        ordering = ['-created_at']

    def __str__(self):
        return self.title