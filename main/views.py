from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import *
from main.serializers import *
from rest_framework import permissions
from django.utils import timezone
from rest_framework.views import APIView
from .tasks import *


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-priority', '-date_finished_planned')
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action=='tasks_by_status':
            status=self.request.data.get('status')
            return super().get_queryset().filter(status=status)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create':
            serializer_class = TaskSerializer
        else:
            serializer_class = TaskListSerializer
        return serializer_class

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            self.queryset = self.queryset.filter(performer_id=user.id)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['performer'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk):
        new_status = request.data.get('new_status')
        task = self.get_object()
        task.status = new_status
        if new_status == Task.COMPLETED:
            task.date_finished = timezone.now()
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['get'])
    def tasks_by_status(self, request):
        return super().list(request)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SendStatisticsView(APIView):
    def post(self, request):
        user = request.user
        tasks = list(user.tasks.all())
        donestasks_count = 0
        for t in tasks:
            if t.status == Task.DONE:
                donestasks_count += 1
        all_tasks_num = len(tasks)
        sucess_coefficicent=donestasks_count/all_tasks_num if all_tasks_num else donestasks_count
        statistics = StatisticsRequest.objects.create(performer=user,
                                                      finished_tasks_num=donestasks_count,
                                                      all_tasks_num=all_tasks_num,
                                                      sucess_coefficicent=sucess_coefficicent)
        send_mail_custom.delay(statistics.id)
        return Response(status=200)
