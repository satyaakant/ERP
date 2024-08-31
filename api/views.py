from rest_framework.response import Response
from rest_framework.decorators import api_view
from mitrr.models import StudentListAdmin, TeacherListAdmin
from .serializers import StudentSerializer, TeacherSerializer

# admin pov
@api_view(['GET'])
def getStudentListAdmin(request):
    students = StudentListAdmin.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addStudentListAdmin(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Student added successfully!"})
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def getTeacherListAdmin(request):
    teachers = TeacherListAdmin.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addTeacherListAdmin(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher added successfully!"})
    return Response(serializer.errors, status=400)
