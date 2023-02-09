from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    class Status(models.IntegerChoices):
        CREATED = 1
        STARTED = 2
        COMPLETED = 3
        DEFERED = 4

    class Priority(models.IntegerChoices):
        DEFAULT = 1
        HIGH = 2

    taskName = models.CharField(max_length = 200)
    taskDescription = models.CharField(max_length = 2000)
    createdAt = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    dueAt = models.DateTimeField(auto_now_add = False, auto_now = False, blank = False)
    status = models.IntegerField(choices=Status.choices, default = 1)
    updatedAt = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    taskLabel = models.CharField(max_length = 100, blank = True, null = True)
    priority = models.IntegerField(choices=Priority.choices, default = 1)

    def __str__(self):
        return self.taskName
