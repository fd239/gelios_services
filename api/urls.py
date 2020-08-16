from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import passport_check


urlpatterns = [
    path('passport_check/', passport_check, name='passport_check'),
]
