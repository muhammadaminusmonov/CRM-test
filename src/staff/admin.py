from django.contrib import admin

from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "middle_name", "status",
        "phone_number", "salary", "born_date", "join_date"
    )
    list_filter = ("status", "join_date", "born_date")
    search_fields = ("first_name", "last_name", "middle_name", "phone_number")
    ordering = ("-join_date",)
    date_hierarchy = "join_date"
    fieldsets = (
        ("Personal Info", {
            "fields": ("first_name", "last_name", "middle_name", "born_date", "phone_number")
        }),
        ("Employment Details", {
            "fields": ("join_date", "salary", "status")
        }),
    )
