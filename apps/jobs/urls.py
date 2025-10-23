from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path("categories/", views.ServiceCategoryListCreateView.as_view(),
         name="categories"),

    # Job Posts (opportunities)
    path("posts/", views.JobPostListCreateView.as_view(),
         name="jobpost-list-create"),
    path("posts/<int:pk>/", views.JobPostRetrieveUpdateDestroyView.as_view(),
         name="jobpost-detail"),

    # Jobs (confirmed bookings)
    path("jobs/", views.JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", views.JobRetrieveUpdateDestroyView.as_view(),
         name="job-detail"),
]
