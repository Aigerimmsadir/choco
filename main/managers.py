
from django.db import models
from django.db.models import Q


class TaskManager(models.Manager):
    def get_my_tasks(self, user_id):
        queryset = self.filter(performer_id=user_id)
        return queryset

