from rest_framework import serializers
from mitrr.models import StudentList, TeacherList, Attendance, Subject, TimeTable
from mitrr.models import Exam, Result, Notification,  Event,  AttendanceReport, Batch



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentList
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherList
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'year', 'section', 'status']

class TimetableSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=TeacherList.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
       model = TimeTable
       fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Exam
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    exam = ExamSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Result
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    receiver = StudentSerializer()  # Assuming notifications are received by students, you can adjust as needed

    class Meta:
        model = Notification
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AttendanceReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = AttendanceReport
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
