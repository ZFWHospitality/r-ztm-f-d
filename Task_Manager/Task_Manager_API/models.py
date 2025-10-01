from django.db import models
from numpy import random
# Create your models here.

class Task(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

