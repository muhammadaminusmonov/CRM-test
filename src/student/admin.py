from django.contrib import admin

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "status",
        "phone_number", "email", "join_date"
    )
    list_filter = ("status", "join_date", "born_date")
    search_fields = (
        "first_name", "last_name", "phone_number", "email",
        "dad_number", "mum_number"
    )
    ordering = ("-join_date",)
    date_hierarchy = "join_date"
    fieldsets = (
        ("Personal Info", {
            "fields": ("first_name", "last_name", "born_date", "status")
        }),
        ("Contact Info", {
            "fields": ("email", "phone_number", "dad_number", "mum_number")
        }),
        ("Enrollment Info", {
            "fields": ("join_date",)
        }),
    )
