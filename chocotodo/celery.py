import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chocotodo.settings")

app = Celery("chocotodo")
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Almaty')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(['main',])