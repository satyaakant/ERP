from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from mitrr.models import StudentList, TeacherList, Attendance, Subject
from .serializers import StudentSerializer, TeacherSerializer, AttendanceSerializer

@api_view(['GET'])
def getStudentList_Mitrr(request):
    # Extracting the query parameters for year and section
    year = request.query_params.get('year')
    section = request.query_params.get('section')

    # Filtering the students based on year and section if provided
    if year and section:
        students = StudentList.objects.filter(year=year, section=section)
    elif year:
        students = StudentList.objects.filter(year=year)
    elif section:
        students = StudentList.objects.filter(section=section)
    else:
        students = StudentList.objects.all()

    # Serializing the filtered student data
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addStudentList_Mitrr(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        unique_field_value = serializer.validated_data.get('email_id')
        if StudentList.objects.filter(email_id=unique_field_value).exists():
            return Response({"error": "Student already exists."}, status=400)
        else:
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

@api_view(['DELETE'])
def deleteStudent_Mitrr(request, enroll_number):
    try:
        student = StudentList.objects.get(enroll_number=enroll_number)
        student.delete()
        return Response({"message": "Student deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except StudentList.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def deleteTeacher_Mitrr(request, teacher_id):
    try:
        teacher = TeacherList.objects.get(teacher_id=teacher_id)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except TeacherList.DoesNotExist:
        return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getAttendanceList_Mitrr(request):
    student_id = request.query_params.get('student_id')
    year = request.query_params.get('year')
    month = request.query_params.get('month')
    subject_id = request.query_params.get('subject_id')
    section = request.query_params.get('section')

    try:
        student = StudentList.objects.get(pk=student_id)
    except StudentList.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        return Response({"error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)

    attendance = Attendance.objects.filter(
        student=student,
        subject=subject,
        date__year=year,
        date__month=month,
        section=section
    )
        
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data)

