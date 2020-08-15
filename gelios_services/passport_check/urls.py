from django.urls import path
from .views import passport_manual_update, passport_auto_update

urlpatterns = [
    path('passport_update/', passport_manual_update, name='passport_update'),
    path('passport_auto_update/', passport_auto_update,
         name='passport_auto_update'),
]
