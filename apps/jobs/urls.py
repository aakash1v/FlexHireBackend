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
    path("posts/my/", views.MyJobPostsView.as_view(), name="my-jobposts"),

    # Jobs (confirmed bookings)
    path("jobs/", views.JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", views.JobRetrieveUpdateDestroyView.as_view(),
         name="job-detail"),

    #application
    path('applications/', views.JobApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.JobApplicationUpdateView.as_view(), name='application-update'),
    path("my-job-applications/", views.MyJobApplicationsView.as_view(), name="my-job-applications"),
]
