from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from main.models import *
from celery import shared_task
from main.tasks import *
import json
