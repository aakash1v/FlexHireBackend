from django.contrib import admin
from .models import ServiceCategory, Job


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "worker",
        "category",
        "status",
        "price",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "category", "created_at")
    search_fields = ("customer__full_name", "worker__full_name", "category__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("customer", "worker", "category", "description", "price", "status")
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

