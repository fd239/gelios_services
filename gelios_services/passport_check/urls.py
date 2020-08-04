from django.urls import path
from .views import passport_manual_update

urlpatterns = [
    path('passport_update/', passport_manual_update, name='passport_update'),
]