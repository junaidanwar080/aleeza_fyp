from django.db import models


class Student(models.Model):
    name_on_certificate = models.CharField(max_length=100, null=False, blank=False)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    cnic = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='students/', null=False, blank=False)
    chinese_name = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=[('男', 'Male'), ('女', 'Female')], null=False, blank=False)
    token_number = models.CharField(max_length=50, null=False, blank=False)
    test_time = models.DateTimeField(null=False, blank=False)
    certificate_no_in_chinese = models.CharField(max_length=100, null=False, blank=False)
    test_type = models.CharField(max_length=10, choices=[('HSK三级', 'HSK3'), ('HSK四级', 'HSK4'), ('HSK五级', 'HSK5')], null=False, blank=False)
    listening_marks = models.IntegerField(null=True, blank=True)
    reading_marks = models.IntegerField(null=True, blank=True)
    writing_marks = models.IntegerField(null=True, blank=True)
    speaking_marks = models.IntegerField( null=True, blank=True)


    def __str__(self):
        return self.name
