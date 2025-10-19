from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    # path('api/workers/', include('apps.workers.urls')),
    # path('api/bookings/', include('apps.bookings.urls')),
    # path('api/chat/', include('apps.chat.urls')),
]

