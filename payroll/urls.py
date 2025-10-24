from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('generate/', views.generate_payroll, name='generate_payroll'),
    path('slip/<int:pk>/', views.salary_slip_pdf, name='salary_slip_pdf'),
    path('export_excel/', views.export_payroll_excel, name='export_payroll_excel'),
]
