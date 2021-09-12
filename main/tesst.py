from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask,PeriodicTasks, IntervalSchedule
import json
from main.models import *
from datetime import datetime,timedelta

from django.contrib.auth.models import User

print([t.name for t in Task.objects.all()])
