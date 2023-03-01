from django.conf.urls import url
from django.urls import path, include

from .views import (
    UserProfileApiView,
    DompetDigitalApiView
)

urlpatterns = [
    path('profile', UserProfileApiView.as_view()),
    path('dompetdigital', DompetDigitalApiView.as_view()),
]