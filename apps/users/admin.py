from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, WorkerProfile, CustomerProfile, Location

# -----------------------
# Custom User Admin
# -----------------------
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "full_name", "phone", "role", "is_verified", "is_staff", "is_active")
    list_filter = ("role", "is_verified", "is_staff", "is_active")
    search_fields = ("email", "full_name", "phone")
    ordering = ("email",)
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        (None, {"fields": ("email", "full_name", "phone", "password")}),
        (_("Personal info"), {"fields": ("role", "bio", "profile_image", "avg_rating", "is_verified")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone", "password1", "password2", "role", "is_active", "is_staff", "is_superuser"),
        }),
    )


# -----------------------
# Worker Profile Admin
# -----------------------
@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_years", "hourly_rate", "work_radius_km", "is_available", "location")
    list_filter = ("is_available", "skills")
    search_fields = ("user__full_name", "user__email")
    readonly_fields = ("updated_at",)


# -----------------------
# Customer Profile Admin
# -----------------------
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "verified_badge", "location")
    list_filter = ("verified_badge",)
    search_fields = ("user__full_name", "user__email")


# -----------------------
# Location Admin
# -----------------------
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "district", "state", "pincode", "lat", "long")
    search_fields = ("city", "district", "state", "pincode")


# -----------------------
# Register User
# -----------------------
admin.site.register(User, UserAdmin)

