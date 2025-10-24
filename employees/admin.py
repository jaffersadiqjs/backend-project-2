from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'department', 'designation', 'salary_per_day')
    search_fields = ('emp_id', 'name', 'department', 'designation')
