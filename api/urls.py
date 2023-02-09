from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListApiView.as_view()),
    path('<int:task_id>/', views.TaskDetailApiView.as_view()),
]
