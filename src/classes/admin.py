from django.contrib import admin

from django.contrib import admin
from .models import Class, Group, Attendance


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("title", "cost_per_month", "duration_per_lesson", "length", "status")
    list_filter = ("status",)
    search_fields = ("title", "description", "length")
    ordering = ("title",)
    fieldsets = (
        ("Class Info", {
            "fields": ("title", "description", "status")
        }),
        ("Financial & Duration", {
            "fields": ("cost_per_month", "duration_per_lesson", "length")
        }),
    )


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ["student"]
    readonly_fields = ["date"]
    can_delete = False


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "classes", "start_at", "end_at", "lesson_per_week", "status")
    list_filter = ("status", "teacher", "classes")
    search_fields = ("name",)
    filter_horizontal = ("student",)
    autocomplete_fields = ["teacher", "classes"]
    inlines = [AttendanceInline]
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "status")
        }),
        ("Schedule", {
            "fields": ("start_at", "end_at", "lesson_per_week")
        }),
        ("Connections", {
            "fields": ("teacher", "classes", "student")
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "group", "date", "status")
    list_filter = ("status", "date", "group")
    search_fields = ("student__first_name", "student__last_name", "group__name")
    autocomplete_fields = ["student", "group"]
    ordering = ("-date",)
