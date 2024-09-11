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

# Batch model
class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.batch_name} "

# StudentList model
class StudentList(models.Model):
    enroll_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)  # Reference to Batch model

    def __str__(self):
        return f"{self.name} - {self.enroll_number}"

# TeacherList model
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
    teacher = models.ForeignKey(TeacherList, on_delete=models.SET_NULL, null=True, blank=True)

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
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)  # Reference to Batch model
    section = models.CharField(max_length=100, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f'{self.student.name} - {self.subject.name} - {self.date} - {self.get_status_display()}'

# TimeTable model
class TimeTable(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    teacher = models.ForeignKey(TeacherList, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    batch = models.CharField(max_length=100, null=True, blank=True)
    semester = models.IntegerField()
    day_of_week = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.teacher} - {self.subject} on {self.day_of_week} ({self.start_time} - {self.end_time})"

# Exam model
class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.IntegerField()
    batch = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    academic_year = models.IntegerField()

    def __str__(self):
        return f"{self.exam_name} for {self.subject.name}"

# Result model
class Result(models.Model):
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} ({self.grade})"

# Notification model
class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.receiver.name} - {self.title}"

# Event model
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.event_name} on {self.date}"

# Attendance Report model
class AttendanceReport(models.Model):
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    total_days = models.IntegerField()
    days_present = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.student.name}'s Attendance Report"
