from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_jobs"
    )
    worker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="worker_jobs"
    )
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, related_name="jobs"
    )
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

