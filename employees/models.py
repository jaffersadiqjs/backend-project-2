from django.db import models

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    salary_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Daily salary in INR")
    date_joined = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.emp_id} - {self.name}"
