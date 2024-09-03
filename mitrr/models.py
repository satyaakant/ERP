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

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    semester = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    year = models.CharField(max_length=100,null=True, blank=True)  # Redundant but flexible
    section = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f'{self.student.name} - {self.subject.name} - {self.date} - {self.get_status_display()}'
