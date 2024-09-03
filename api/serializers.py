from rest_framework import serializers
from mitrr.models import StudentList, TeacherList,Attendance,Subject

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

