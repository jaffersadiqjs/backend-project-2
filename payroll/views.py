from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from calendar import monthrange
from .models import Payroll
from employees.models import Employee
from attendance.models import Attendance
from .utils import generate_salary_slip_pdf, export_payrolls_to_excel
from django.db import IntegrityError

def payroll_list(request):
    qs = Payroll.objects.select_related('employee').all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': qs})

def generate_payroll(request):
    # Generate payroll for current month by default; can be extended to accept month/year
    today = date.today()
    month = today.month
    year = today.year
    total_days = monthrange(year, month)[1]

    generated = []
    for emp in Employee.objects.all():
        present_days = Attendance.objects.filter(employee=emp, date__year=year, date__month=month, status='Present').count()
        net_salary = emp.salary_per_day * present_days
        try:
            p, created = Payroll.objects.update_or_create(
                employee=emp, month=month, year=year,
                defaults={'total_days': total_days, 'present_days': present_days, 'net_salary': net_salary}
            )
            generated.append(p)
        except IntegrityError:
            # ignore duplicates in rare race
            pass

    return render(request, 'payroll/payroll_generate.html', {'payrolls': generated, 'month': month, 'year': year})

def salary_slip_pdf(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    return generate_salary_slip_pdf(payroll)

def export_payroll_excel(request):
    qs = Payroll.objects.select_related('employee').all()
    return export_payrolls_to_excel(qs)
