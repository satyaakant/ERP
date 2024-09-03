from django.db import models
import uuid

# User model
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

# Custom session model
class CustomSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100)
    userdata = models.JSONField()
    jwttoken = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Session for {self.user.username}"

# Student list model
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

# Teacher list model
class TeacherList(models.Model):
    teacher_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    subjects = models.JSONField()
    email_id = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.teacher_id}"

# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    semester = models.IntegerField()
    year = models.IntegerField()
    teacher = models.ForeignKey(TeacherList, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Teacher

    def __str__(self):
        return f"{self.name} ({self.code}) - Taught by {self.teacher.name if self.teacher else 'No teacher assigned'}"

# Attendance model
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    year = models.CharField(max_length=100, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)  # Added semester field
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f'{self.student.name} - {self.subject.name} - {self.date} - {self.get_status_display()}'
