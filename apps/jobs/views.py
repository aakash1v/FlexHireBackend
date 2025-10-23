from rest_framework import generics, permissions, filters
from .models import ServiceCategory, JobPost, Job
from .serializers import ServiceCategorySerializer, JobPostSerializer, JobSerializer


# --- CATEGORY VIEWS ---
class ServiceCategoryListCreateView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]


# --- JOB POST VIEWS ---
class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by("-created_at")
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "location", "category__name"]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        job_post = self.get_object()
        if job_post.customer != self.request.user:
            raise PermissionError("You can only edit your own job posts.")
        serializer.save()


# --- JOB VIEWS ---
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        job = self.get_object()
        user = self.request.user

        # Allow only customer or assigned worker to modify
        if user != job.customer and user != job.worker:
            raise PermissionError("You are not authorized to edit this job.")
        serializer.save()
