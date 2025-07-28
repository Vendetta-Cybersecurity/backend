from django.urls import path
from . import views

urlpatterns = [
    path('empty/', views.empty_json, name='empty-json'),
    path('status/', views.api_status, name='api-status'),
]