from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["taskName", "taskDescription", "createdAt", "dueAt", "status", "updatedAt", "user", "priority", "taskLabel"]
