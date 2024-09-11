from rest_framework import serializers
from mitrr.models import (
    StudentList, TeacherList, Attendance, Subject, TimeTable,
    Exam, Result, Notification, Event, AttendanceReport, Batch
)


# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentList
        fields = '__all__'


# Teacher serializer
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherList
        fields = '__all__'


# Subject serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


# Attendance serializer
class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nesting Student Serializer
    subject = SubjectSerializer()  # Nesting Subject Serializer

    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'batch', 'section', 'status']  # Added 'batch' field


# Timetable serializer
class TimetableSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=TeacherList.objects.all())  # Related field for teacher
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())  # Related field for subject

    class Meta:
        model = TimeTable
        fields = '__all__'


# Exam serializer
class ExamSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()  # Nesting Subject Serializer

    class Meta:
        model = Exam
        fields = '__all__'


# Result serializer
class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nesting Student Serializer
    exam = ExamSerializer()  # Nesting Exam Serializer
    subject = SubjectSerializer()  # Nesting Subject Serializer

    class Meta:
        model = Result
        fields = '__all__'


# Notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    receiver = StudentSerializer()  # Assuming notifications are received by students, you can adjust as needed

    class Meta:
        model = Notification
        fields = '__all__'


# Event serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


# Attendance report serializer
class AttendanceReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nesting Student Serializer

    class Meta:
        model = AttendanceReport
        fields = '__all__'


# Batch serializer
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['batch_name', 'year', 'description', 'semester']
