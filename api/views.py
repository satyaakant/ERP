from rest_framework.response import Response
from rest_framework.decorators import api_view
from mitrr.models import StudentList, TeacherList
from .serializers import StudentSerializer, TeacherSerializer

# mitrr pov
@api_view(['GET'])
def getStudentList_Mitrr(request):
    students = StudentList.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addStudentList_Mitrr(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Student added successfully!"})
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def getTeacherList_Mitrr(request):
    teachers = TeacherList.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addTeacherList_Mitrr(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        unique_field_value = serializer.validated_data.get('email_id')
        if TeacherList.objects.filter(email_id=unique_field_value).exists():
            return Response({"error": "Teacher already exists."}, status=400)
        else:
            serializer.save()
            return Response({"message": "Teacher added successfully!"}, status=200)
    
    return Response(serializer.errors, status=400)
