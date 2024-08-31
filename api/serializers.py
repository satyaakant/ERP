from rest_framework import serializers
from mitrr.models import StudentList, TeacherList

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentList
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherList
        fields = '__all__'
