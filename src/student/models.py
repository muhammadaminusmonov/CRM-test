from django.db import models

class Student(models.Model):
    STATUS_CHOICES = [
        (1, "Active"),
        (2, "Inactive"),
        (3, "Graduated"),
        (4, "On hold"),
    ]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    born_date = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=150)
    dad_number = models.CharField(max_length=150)
    mum_number = models.CharField(max_length=150)
    join_date = models.DateField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.first_name

    def initials(self):
        return (self.first_name[0] + self.last_name[0]).upper()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"