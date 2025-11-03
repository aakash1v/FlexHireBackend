from apps.utils.email_utils import send_application_status_email
from rest_framework import generics, permissions, filters
from .models import ServiceCategory, JobPost, Job
from .serializers import ServiceCategorySerializer, JobPostSerializer, JobSerializer
# views.py
from .models import JobApplication
from .serializers import JobApplicationSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class JobApplicationListCreateView(generics.ListCreateAPIView):
    """
    GET: List all applications (for logged-in worker)
    POST: Apply to a job post
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_staff') and user.is_staff:
            return JobApplication.objects.all()
        return JobApplication.objects.filter(worker=user)

    def perform_create(self, serializer):
        serializer.save(worker=self.request.user)


class MyJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # show all applications made to this customer's job posts
        user = self.request.user
        return JobApplication.objects.filter(job_post__customer=user).order_by("-applied_at")


class JobApplicationUpdateView(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        app = self.get_object()
        if app.job_post.customer != request.user:
            raise PermissionDenied(
                "You are not allowed to update this application.")

        status_choice = request.data.get('status')
        if status_choice not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        app.status = status_choice
        app.save()

        # Notify worker
        send_application_status_email(
            worker_email=app.worker.email,
            worker_name=app.worker.full_name,
            job_title=app.job_post.title,
            status=status_choice
        )

        # If accepted, create Job automatically
        if status_choice == 'accepted':
            Job.objects.create(
                post=app.job_post,
                customer=app.job_post.customer,
                worker=app.worker,
                category=app.job_post.category,
                description=app.job_post.description,
                price=app.job_post.pay_rate,
                status='accepted'
            )

        return Response(JobApplicationSerializer(app).data)


# --- CATEGORY VIEWS ---
class ServiceCategoryListCreateView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]


# --- JOB POST VIEWS ---
class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by("-created_at")
    serializer_class = JobPostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "location", "category__name"]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS → allow everyone
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class MyJobPostsView(generics.ListAPIView):
    """
    List all job posts created by the authenticated user
    """
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(customer=self.request.user).order_by("-created_at")


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
