from django.db import models

# Create your models here.
class StudentListAdmin(models.Model):
    enroll_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.enroll_number}"
    
class TeacherListAdmin(models.Model):
    teacher_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    subjects = models.JSONField()
    email_id = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

