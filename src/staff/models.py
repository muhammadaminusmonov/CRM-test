from django.db import models

class Staff(models.Model):
    STATUS_CHOICES = [
        (1, "Active"),
        (2, "Inactive"),
        (3, "Holiday"),
        (4, "Fired"),
        (5, "Retired"),
        (6, "On hold")
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    born_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=11)
    join_date = models.DateField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.first_name