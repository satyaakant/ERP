from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    enroll_number = models.CharField(max_length=100, unique=True)
    section = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.enroll_number})"

    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

# Custom session model
class CustomSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100)  
    userdata = models.JSONField() 
    jwttoken = models.UUIDField(default=uuid.uuid4, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Session for {self.student.username} - {self.jwttoken}"
