from django.contrib import admin

from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "age", "status",
        "phone_number", "email", "fixed_salary", "salary", "percentage"
    )
    list_filter = ("status", "fixed_salary")
    search_fields = (
        "first_name", "last_name", "phone_number", "email", "address"
    )
    ordering = ("first_name",)
    fieldsets = (
        ("Personal Info", {
            "fields": ("first_name", "last_name", "age", "status")
        }),
        ("Contact Info", {
            "fields": ("phone_number", "email", "address")
        }),
        ("Salary Info", {
            "fields": ("fixed_salary", "salary", "percentage")
        }),
    )
