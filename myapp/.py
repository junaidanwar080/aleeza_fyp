from django.urls import path
from . import views

urlpatterns = [
    # ------------------------
    # Static pages
    # ------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ------------------------
    # Student CRUD
    # ------------------------
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # ------------------------
    # Department CRUD
    # ------------------------
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/edit/<int:pk>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:pk>/', views.delete_department, name='delete_department'),
]
