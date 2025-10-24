from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_create, name='employee_create'),
    path('edit/<int:pk>/', views.employee_update, name='employee_update'),
    path('detail/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
]
