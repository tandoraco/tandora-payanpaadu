from django.urls import path

from .views import execute_background_task

urlpatterns = [
    path('tasks/execute/', execute_background_task, name='background-task-executor'),
]
