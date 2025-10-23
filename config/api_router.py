
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include('apps.users.urls')),
    path('jobs/', include('apps.jobs.urls')),
    # path('api/chat/', include('apps.chat.urls')),
]
