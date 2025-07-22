from django.db import models

class Teacher(models.Model):
    STATUS_CHOICES = [
        (1, "Working"),
        (2, "On holiday"),
        (3, "Fired"),
        (4, "Sick"),
        (5, "Not working"),
    ]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    age = models.SmallIntegerField()
    phone_number = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.TextField()
    fixed_salary = models.BooleanField(default=True)
    salary = models.BigIntegerField()
    percentage = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.first_name

class Teacher(models.Model):
    STATUS_CHOICES = [
        (1, "Working"),
        (2, "On holiday"),
        (3, "Fired"),
        (4, "Sick"),
        (5, "Not working"),
    ]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    age = models.SmallIntegerField()
    phone_number = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.TextField()
    fixed_salary = models.BooleanField(default=True)
    salary = models.BigIntegerField()
    percentage = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.first_name

    def full_name(self):
        return f"{self.first_name} {self.last_name}"