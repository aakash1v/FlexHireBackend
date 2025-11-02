
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
    path("users/me", views.MeView.as_view(), name="user-me"),
    path("users/me/photo", views.UploadProfilePhotoView.as_view(), name="user-photo"),
    path("users/<uuid:id>", views.PublicUserView.as_view(), name="user-public"),
]
