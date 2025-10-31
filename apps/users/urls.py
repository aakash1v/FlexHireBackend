
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    path('google_login/', views.google_auth),
    path('signup/', views.SignupView.as_view(),
         name='custom_signup'),
    path('verify-otp/', views.verify_otp),
]
