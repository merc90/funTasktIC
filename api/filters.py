from django_filters import rest_framework as filters
from .models import Task


# We create filters for each field we want to be able to filter on
class TaskFilter(filters.FilterSet):
    taskName = filters.CharFilter(lookup_expr='icontains')
    status = filters.NumberFilter()
    priority = filters.NumberFilter()
    due__gt = filters.NumberFilter(field_name='dueAt', lookup_expr='gt')
    due__lt = filters.NumberFilter(field_name='dueAt', lookup_expr='lt')
    user = filters.NumberFilter()

    class Meta:
        model = Task
        fields = ['taskName', 'status', 'priority', 'due__gt', 'due__lt', 'user', 'taskLabel']
