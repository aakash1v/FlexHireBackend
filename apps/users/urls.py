
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
]

