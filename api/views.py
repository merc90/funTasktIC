from dateutil import parser
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, filters
from .models import Task
from .serializers import TaskSerializer

class TaskListApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'priority', 'taskName', 'taskLabel', 'dueAt']

    #  List all tasks
    def get(self, request, *args, **kwargs):
        '''
        List all the tasks for given requested user
        '''
        tasks = Task.objects.filter(user = self.request.user.id)
        get_params = request.query_params
        for field in self.filterset_fields:
            if field in get_params:
                tasks = Task.objects.filter(**{field: get_params[field]})
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  Create task(s)
    def post(self, request, *args, **kwargs):
        '''
        Create the Task with given task data
        '''
        repeat = request.data.get('repeat') if request.data.get('repeat') is not None else 1
        dueAt = request.data.get('dueAt')
        data_array = []
        for i in range(0, repeat):
            dueAtRepeat = parser.parse(dueAt) + timedelta(days=7*i)
            data = {
                'taskName': request.data.get('taskName'),
                'taskDescription': request.data.get('taskDescription'),
                'createdAt': request.data.get('createdAt'),
                'dueAt': dueAtRepeat,
                'status': request.data.get('status'),
                'updatedAt': request.data.get('updatedAt'), 
                'user': request.user.id,
                'priority': request.data.get('priority'),
                'taskLabel': request.data.get('taskLabel')
            }
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data_array.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data_array, status=status.HTTP_201_CREATED)

class TaskDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, task_id, user_id):
        '''
        Helper method to get the object with given task_id, and user_id
        '''
        try:
            return Task.objects.get(id=task_id, user = user_id)
        except Task.DoesNotExist:
            return None

    #  Retrieve task
    def get(self, request, task_id, *args, **kwargs):
        '''
        Retrieves the Task with given task_id
        '''
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  Update task
    def put(self, request, task_id, *args, **kwargs):
        '''
        Updates the task item with given task_id if exists
        '''
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'taskName': request.data.get('taskName'),
            'taskDescription': request.data.get('taskDescription'),
            'createdAt': request.data.get('createdAt'),
            'dueAt': request.data.get('dueAt'),
            'status': request.data.get('status'),
            'updatedAt': request.data.get('updatedAt'),
            'user': request.user.id,
            'priority': request.data.get('priority'),
            'taskLabel': request.data.get('taskLabel')
        }
        serializer = TaskSerializer(instance = task_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  Delete task
    def delete(self, request, task_id, *args, **kwargs):
        '''
        Deletes the task item with given task_id if exists
        '''
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {"res": "Object with task id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
