from django.contrib import admin

from .models import Job, JobApplication, JobPost, ServiceCategory


# -----------------------
# SERVICE CATEGORY ADMIN
# -----------------------
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# -----------------------
# JOB POST ADMIN (Customer posts work opportunities)
# -----------------------
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "customer",
        "category",
        "location",
        "num_workers_required",
        "pay_rate",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "category",
        "food_provided",
        "tea_provided",
        "accommodation_provided",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "customer__full_name",
        "location",
        "category__name",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("customer", "category", "title", "description", "location")},
        ),
        (
            "Work Details",
            {
                "fields": (
                    "work_days",
                    "work_hours",
                    "num_workers_required",
                    "pay_rate",
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Perks & Offerings",
            {
                "fields": ("food_provided", "tea_provided", "accommodation_provided"),
                "classes": ("collapse",),
            },
        ),
        ("Status & Timestamps", {"fields": ("status", "created_at", "updated_at")}),
    )


# -----------------------
# JOB ADMIN (Confirmed work between customer & worker)
# -----------------------
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "customer",
        "worker",
        "category",
        "status",
        "price",
        "created_at",
    )
    list_filter = ("status", "category", "created_at")
    search_fields = (
        "customer__full_name",
        "worker__full_name",
        "category__name",
        "post__title",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        ("Linked Post", {"fields": ("post",)}),
        ("Participants", {"fields": ("customer", "worker", "category")}),
        ("Job Details", {"fields": ("description", "price", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


admin.site.register(JobApplication)
