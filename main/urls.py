
from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter() 
router.register(r'task', TaskViewSet, basename='task')
router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('send_statistics/', SendStatisticsView.as_view())
]
