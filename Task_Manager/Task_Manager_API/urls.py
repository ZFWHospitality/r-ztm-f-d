from django.urls import path
from Task_Manager_API import views

urlpatterns = [
    path('', views.view_dtl, name='dtl'),
    path('tasks/', views.view_Task, name='view_Task'),
    path('tasks/<int:pk>/', views.TaskByID, name='TaskByID'),
]