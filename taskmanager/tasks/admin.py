
from django.contrib import admin
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title", "description", "owner__username")

