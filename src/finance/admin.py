from django.contrib import admin

from django.contrib import admin
from .models import (
    Payment, Expanses, TeacherSalary,
    StaffSalary, Cost, Profit
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("student", "amount", "paid_for_month", "paid_at", "to_group", "to_teacher")
    list_filter = ("paid_at", "to_group", "to_teacher")
    search_fields = ("student__first_name", "student__last_name", "to_group__name", "to_teacher__first_name")
    autocomplete_fields = ["student", "to_group", "to_teacher"]
    date_hierarchy = "paid_at"
    ordering = ("-paid_at",)


@admin.register(Expanses)
class ExpansesAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("name", "description")
    date_hierarchy = "date"
    ordering = ("-date",)


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ("teacher", "month", "salary", "paid", "paid_date")
    list_filter = ("month",)
    search_fields = ("teacher__first_name", "teacher__last_name")
    autocomplete_fields = ["teacher"]
    date_hierarchy = "paid_date"
    ordering = ("-month",)


@admin.register(StaffSalary)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = ("staff", "month", "salary", "paid", "paid_date")
    list_filter = ("month",)
    search_fields = ("staff__first_name", "staff__last_name")
    autocomplete_fields = ["staff"]
    date_hierarchy = "paid_date"
    ordering = ("-month",)


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ("month", "total_teacher_cost", "total_staff_cost", "total_cost", "staff", "teacher", "expanses")
    list_filter = ("month",)
    search_fields = ("teacher__first_name", "staff__first_name")
    autocomplete_fields = ["teacher", "staff", "expanses"]
    date_hierarchy = "month"
    ordering = ("-month",)


@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    list_display = ("month", "payment", "cost", "gross_profit", "profit")
    list_filter = ("month",)
    autocomplete_fields = ["payment", "cost"]
    date_hierarchy = "month"
    ordering = ("-month",)
