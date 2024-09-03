from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from mitrr.models import StudentList, TeacherList, Attendance, Subject
from .serializers import StudentSerializer, TeacherSerializer, AttendanceSerializer
from datetime import datetime  # Import datetime for date parsing

# View to get a list of students with optional filtering by year and section
@api_view(['GET'])
def getStudentList_Mitrr(request):
    year = request.query_params.get('year')
    section = request.query_params.get('section')

    if year and section:
        students = StudentList.objects.filter(year=year, section=section)
    elif year:
        students = StudentList.objects.filter(year=year)
    elif section:
        students = StudentList.objects.filter(section=section)
    else:
        students = StudentList.objects.all()

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# View to add a new student to the list
@api_view(['POST'])
def addStudentList_Mitrr(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        unique_field_value = serializer.validated_data.get('email_id')
        if StudentList.objects.filter(email_id=unique_field_value).exists():
            return Response({"error": "Student already exists."}, status=400)
        else:
            serializer.save()
            return Response({"message": "Student added successfully!"}, status=200)
    return Response(serializer.errors, status=400)

# View to delete a student by enrollment number
@api_view(['DELETE'])
def deleteStudent_Mitrr(request, enroll_number):
    try:
        student = StudentList.objects.get(enroll_number=enroll_number)
        student.delete()
        return Response({"message": "Student deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except StudentList.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

# View to get a list of teachers with their associated subjects
@api_view(['GET'])
def getTeacherList_Mitrr(request):
    teachers = TeacherList.objects.all()
    
    teacher_data = []
    for teacher in teachers:
        subjects = Subject.objects.filter(teacher=teacher)
        subjects_data = [{"name": subject.name, "code": subject.code, "semester": subject.semester, "year": subject.year} for subject in subjects]

        teacher_data.append({
            "teacher_id": teacher.teacher_id,
            "name": teacher.name,
            "email_id": teacher.email_id,
            "phone_number": teacher.phone_number,
            "subjects": subjects_data
        })

    return Response(teacher_data)

# View to add a new teacher to the list
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

# View to delete a teacher by teacher ID
@api_view(['DELETE'])
def deleteTeacher_Mitrr(request, teacher_id):
    try:
        teacher = TeacherList.objects.get(teacher_id=teacher_id)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except TeacherList.DoesNotExist:
        return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

# View to get attendance records based on student, subject, and date
@api_view(['GET'])
def getAttendanceList_Mitrr(request, year):
    enroll_number = request.query_params.get('enroll_number')
    month = request.query_params.get('month')
    subject_id = request.query_params.get('subject_id')
    section = request.query_params.get('section')
    semester = request.query_params.get('semester')

    # Check if enroll_number is provided
    if not enroll_number:
        return Response({"error": "Missing enroll_number in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate and fetch student
    try:
        student = StudentList.objects.get(enroll_number=enroll_number, year=year)
    except StudentList.DoesNotExist:
        return Response({"error": f"Student with enrollment number {enroll_number} not found for year {year}."}, status=status.HTTP_404_NOT_FOUND)

    # Check if subject_id is provided and valid
    if subject_id:
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": f"Subject with ID {subject_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Missing subject_id in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter attendance records based on provided criteria
    attendance = Attendance.objects.filter(
        student=student,
        subject=subject,
        date__month=month,
        section=section,
        semester=semester
    )

    if not attendance.exists():
        return Response({"error": "No attendance records found for the provided criteria."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data)

# Additional View to filter attendance based on multiple criteria
@api_view(['GET'])
def getFilteredAttendanceList(request):
    year = request.query_params.get('year')
    subject_id = request.query_params.get('subject_id')
    section = request.query_params.get('section')
    semester = request.query_params.get('semester')

    # Filter attendance based on the given criteria
    attendance = Attendance.objects.all()
    
    if year:
        attendance = attendance.filter(year=year)
    if subject_id:
        attendance = attendance.filter(subject_id=subject_id)
    if section:
        attendance = attendance.filter(section=section)
    if semester:
        attendance = attendance.filter(semester=semester)
    
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data)

# View to add a new attendance record
@api_view(['POST'])
def addAttendance(request):
    # Extract data from the request
    enroll_number = request.data.get('enroll_number')
    subject_id = request.data.get('subject_id')
    date = request.data.get('date')
    year = request.data.get('year')
    section = request.data.get('section')
    semester = request.data.get('semester')
    status_code = request.data.get('status', 'P')  # Default to 'Present' if not provided

    # Validate and fetch student
    try:
        student = StudentList.objects.get(enroll_number=enroll_number)
    except StudentList.DoesNotExist:
        return Response({"error": f"Student with enrollment number {enroll_number} not found."}, status=status.HTTP_404_NOT_FOUND)

    # Validate and fetch subject
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        return Response({"error": f"Subject with ID {subject_id} not found."}, status=status.HTTP_404_NOT_FOUND)

    # Validate date format using datetime
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if attendance already exists for the given student, subject, and date
    if Attendance.objects.filter(student=student, subject=subject, date=parsed_date).exists():
        return Response({"error": "Attendance record already exists for this student, subject, and date."}, status=status.HTTP_400_BAD_REQUEST)

    # Create new attendance record
    attendance = Attendance(
        student=student,
        subject=subject,
        date=parsed_date,
        year=year,
        section=section,
        semester=semester,
        status=status_code
    )
    attendance.save()

    return Response({"message": "Attendance added successfully!"}, status=status.HTTP_201_CREATED)
