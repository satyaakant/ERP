from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class CustomSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100)
    userdata = models.JSONField()
    jwttoken = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Session for {self.user.username}"

class StudentList(models.Model):
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
    
class TeacherList(models.Model):
    teacher_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    subjects = models.JSONField()
    email_id = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.teacher_id}"

