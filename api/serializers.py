from rest_framework import serializers
from mitrr.models import StudentListAdmin, TeacherListAdmin

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentListAdmin
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherListAdmin
        fields = '__all__'
