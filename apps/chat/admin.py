from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "sender",
        "receiver",
        "text_preview",
        "timestamp",
        "is_read",
    )
    list_filter = ("is_read", "timestamp")
    search_fields = ("sender__full_name", "receiver__full_name", "text")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)

    def text_preview(self, obj):
        return (obj.text[:50] + "...") if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Message"

