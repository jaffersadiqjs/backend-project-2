from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from django import forms

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['emp_id', 'name', 'department', 'designation', 'salary_per_day', 'date_joined']

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})
    qs = Employee.objects.all().order_by('emp_id')
    return render(request, 'employees/employee_list.html', {'employees': qs})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})

def employee_update(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_list')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee'})

def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': emp})

def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_detail.html', {'employee': emp, 'confirm_delete': True})
