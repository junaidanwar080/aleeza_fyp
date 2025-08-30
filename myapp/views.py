from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.http import HttpResponse
import os
from django.conf import settings

# -------------------------
# Static Pages
# -------------------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# -------------------------
# Student List
# -------------------------
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# -------------------------
# Student Detail
# -------------------------
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    total = (student.listening_marks or 0) + (student.reading_marks or 0) + (student.writing_marks or 0)

    return render(request, 'student_detail.html', {'student': student,'total': total})

# -------------------------
# Create Student
# -------------------------
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('student_list')
        else:
            print("Form Errors ❌:", form.errors)
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

# -------------------------
# Update Student
# -------------------------
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form, 'student': student})

# -------------------------
# Delete Student
# -------------------------
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


# -------------------------
# Student QR Code
# -------------------------
def generate_qr(request, pk):
    base_url = request.build_absolute_uri('/')  # e.g. http://127.0.0.1:8000/

    url = f"{base_url}students/{pk}/"   # This will open when user scans QR
    qr = qrcode.make(url)

    # Save to BytesIO (for response)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    # Save to media folder
    file_name = f"qr_id_{pk}.png"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    qr.save(file_path)   # Save the QR code image

    # Return the QR in response (browser will just show it)
    return HttpResponse(buffer.getvalue(), content_type="image/png")