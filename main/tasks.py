from celery import shared_task
from main.models import *
import datetime
from django.core.mail import send_mail
from django.utils import timezone
from chocotodo.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User


@shared_task(name="send_mail_custom")
def send_mail_custom(statistics_id):
    statistics = StatisticsRequest.objects.select_related(
        'performer').get(id=statistics_id)
    user = statistics.performer
    email_header='Statistics'
    email_text = 'Finished_tasks={},\nAll tasks={},\nSuccess coefficient={}'.format(
        statistics.finished_tasks_num,
        statistics.all_tasks_num,
        statistics.sucess_coefficicent)
    email = user.email
    print(email_text,EMAIL_HOST_USER,email)
    send_mail(
        email_header,
        email_text,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print('sent')