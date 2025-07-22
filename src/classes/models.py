from django.db import models
from student.models import Student
from teacher.models import Teacher


class Class(models.Model):
    STATUS_CHOICES = [
        (1, "Active"),
        (2, "Inactive"),
    ]
    title = models.CharField(max_length=255)
    cost_per_month = models.BigIntegerField()
    duration_per_lesson = models.TimeField()
    length = models.CharField(max_length=150)
    description = models.TextField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.title

class Group(models.Model):
    STATUS_CHOICES = [
        (1, "Active"),
        (2, "Completed"),
        (3, "Closed"),
        (4, "On hold"),
    ]

    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    student = models.ManyToManyField(Student, related_name="student_group")
    classes = models.ForeignKey(Class, on_delete=models.PROTECT, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    lesson_per_week = models.SmallIntegerField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = [
        (1, "Present"),
        (2, "Absent"),
        (3, "Excused"),
        (4, "Late"),
    ]
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    date = models.DateTimeField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.status