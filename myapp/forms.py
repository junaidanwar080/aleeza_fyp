from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # Sab fields include honge
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(),
            'test_type': forms.Select(),
            'test_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'name_on_certificate': 'Name (English)',
            'father_name': 'Father Name (English)',
            'address': 'Center Address (Chinese)',
            'nationality': 'Nationality (Chinese)',
            'cnic': 'CNIC / Passport No',
        }
