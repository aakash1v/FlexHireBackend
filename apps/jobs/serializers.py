from .models import JobApplication, Job
from rest_framework import serializers
from .models import ServiceCategory, JobPost, Job


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "description"]


class JobPostSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.username", read_only=True)
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    class Meta:
        model = JobPost
        fields = [
            "id",
            "title",
            "description",
            "location",
            "category",
            "category_name",
            "customer",
            "customer_name",
            "work_days",
            "work_hours",
            "num_workers_required",
            "pay_rate",
            "start_date",
            "end_date",
            "food_provided",
            "tea_provided",
            "accommodation_provided",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "created_at", "updated_at", "customer"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["customer"] = request.user
        return super().create(validated_data)


class JobSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.username", read_only=True)
    worker_name = serializers.CharField(
        source="worker.username", read_only=True)
    category_name = serializers.CharField(
        source="category.name", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "post",
            "post_title",
            "customer",
            "customer_name",
            "worker",
            "worker_name",
            "category",
            "category_name",
            "description",
            "price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# serializers.py


class JobApplicationSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(
        source='worker.full_name', read_only=True)
    job_post_title = serializers.CharField(
        source='job_post.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'job_post',
            'worker',
            'worker_name',
            'job_post_title',
            'message',
            'status',
            'applied_at',
        ]
        read_only_fields = ['status', 'worker']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['worker'] = request.user
        return super().create(validated_data)
