from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name_on_certificate", "father_name", "cnic")
    search_fields = ("name_on_certificate", "father_name", "cnic")

