from django.urls import path
from .views import passport_update

urlpatterns = [
    path('passport_update', passport_update, name='passport_update'),
]