from django.contrib import admin
from .models import Payroll

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'present_days', 'net_salary')
    list_filter = ('month', 'year')
    search_fields = ('employee__emp_id', 'employee__name')
