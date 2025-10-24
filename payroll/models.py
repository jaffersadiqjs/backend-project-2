from django.db import models
from employees.models import Employee

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    total_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.emp_id} - {self.month}/{self.year}"
