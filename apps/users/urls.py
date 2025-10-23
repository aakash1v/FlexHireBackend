
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('google_login/', views.google_auth),
    path('signup/', views.signup, name='custom_signup'),  # for React
]

