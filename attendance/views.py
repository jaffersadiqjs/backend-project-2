from django.shortcuts import render, redirect
from datetime import date
from .models import Attendance
from employees.models import Employee
from django import forms
from django.db import IntegrityError

class MarkForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    date = forms.DateField(initial=date.today)
    status = forms.ChoiceField(choices=Attendance.STATUS_CHOICES)

def attendance_list(request):
    qs = Attendance.objects.select_related('employee').all().order_by('-date')[:200]
    return render(request, 'attendance/attendance_list.html', {'attendances': qs})

def mark_attendance(request):
    message = ''
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            emp = form.cleaned_data['employee']
            dt = form.cleaned_data['date']
            status = form.cleaned_data['status']
            try:
                Attendance.objects.create(employee=emp, date=dt, status=status)
                message = 'Attendance marked.'
            except IntegrityError:
                message = 'Attendance for this employee on this date already exists.'
    else:
        form = MarkForm()
    return render(request, 'attendance/attendance_list.html', {'form': form, 'message': message, 'attendances': Attendance.objects.select_related('employee').all().order_by('-date')[:200]})
