from django.urls import path
from . import views

urlpatterns = [
    # -------------------------
    # Static Pages
    # -------------------------
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # -------------------------
    # Student URLs
    # -------------------------
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),  # Add new student
    path('students/<int:pk>/', views.student_detail, name='student_detail'),  # View student detail
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),  # Edit student
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),  # Delete student
    path('students/<int:pk>/qr/', views.generate_qr, name='generate_qr'),  # Delete student

]
