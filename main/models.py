from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime, timedelta
from django.utils import timezone
from main.managers import *


def return_date_time():
    now = timezone.now()
    return now + timedelta(days=7)


class Task(models.Model):
    TO_DO = 0
    IN_PROGRESS = 1
    DONE = 2
    LOW_PRIORITY = 0
    MIDDLE_PRIORITY = 1
    HIGH_PRIOIRTY = 2
    STATES = (
        (TO_DO, 'TO_DO'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (DONE, 'DONE')
    )
    PRIORITIES = (
        (LOW_PRIORITY, 'LOW_PRIORITY'),
        (MIDDLE_PRIORITY, 'MIDDLE_PRIORITY'),
        (HIGH_PRIOIRTY, 'HIGH_PRIOIRTY')
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    performer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='tasks', null=True)
    status = models.PositiveSmallIntegerField(default=TO_DO, choices=STATES)
    priority = models.PositiveSmallIntegerField(
        default=MIDDLE_PRIORITY, choices=PRIORITIES)
    date_created = models.DateTimeField(default=timezone.now)
    date_finished = models.DateTimeField(null=True)
    # automatically is in 7 days after the start
    date_finished_planned = models.DateTimeField(default=return_date_time)
    objects = TaskManager()


class StatisticsRequest(models.Model):
    date_created = models.DateTimeField(auto_now=True, null=True)
    performer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='statistic_requests', null=True)
    finished_tasks_num = models.IntegerField(default=0)
    all_tasks_num = models.IntegerField(default=0)
    sucess_coefficicent = models.FloatField(default=1)
