from rest_framework.response import Response
from rest_framework.decorators import api_view
from mitrr.models import StudentList, TeacherList
from .serializers import StudentSerializer, TeacherSerializer

# admin pov
@api_view(['GET'])
def getStudentList(request):
    students = StudentList.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addStudentList(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Student added successfully!"})
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def getTeacherList(request):
    teachers = TeacherList.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addTeacherList(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher added successfully!"})
    return Response(serializer.errors, status=400)
