from django.db import models

from student.models import Student
from classes.models import Group
from teacher.models import Teacher
from staff.models import Staff


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paid_at = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_for_month = models.DecimalField(max_digits=10, decimal_places=2)
    to_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    to_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.amount

class Expanses(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TeacherSalary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    month = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()

    def __str__(self):
        return self.salary

class StaffSalary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    month = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()

    def __str__(self):
        return self.salary

    @property
    def status(self):
        if self.paid == self.salary:
            return 'paid'
        elif self.paid > 0:
            return 'partial'
        return 'unpaid'

class Cost(models.Model):
    month = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    total_teacher_cost = models.DecimalField(max_digits=15, decimal_places=2)
    total_staff_cost = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    expanses = models.ForeignKey(Expanses, on_delete=models.PROTECT)

    def __str__(self):
        return self.total_cost

class Profit(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    cost = models.ForeignKey(Cost, on_delete=models.PROTECT)
    gross_profit = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=20, decimal_places=2)
    month = models.DateField()

    def __str__(self):
        return self.gross_profit