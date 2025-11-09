from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    post = models.ForeignKey("JobPost", on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_jobs")
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="worker_jobs")
    category = models.ForeignKey("ServiceCategory", on_delete=models.SET_NULL, null=True, related_name="jobs")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job {self.id} - {self.customer} → {self.worker} ({self.status})"


class JobPost(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_jobs")
    category = models.ForeignKey(
        "ServiceCategory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="job_posts",
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=255)

    # Work details
    work_days = models.CharField(max_length=100, blank=True)  # e.g. "Mon-Fri"
    work_hours = models.CharField(max_length=100, blank=True)  # e.g. "9am - 5pm"
    num_workers_required = models.PositiveIntegerField(default=1)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Additional offerings (optional perks)
    food_provided = models.BooleanField(default=False)
    tea_provided = models.BooleanField(default=False)
    accommodation_provided = models.BooleanField(default=False)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="open",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"


class JobApplication(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applications")
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applications")
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job_post", "worker")  # prevent multiple applications

    def __str__(self):
        return f"{self.worker} → {self.job_post.title} ({self.status})"
