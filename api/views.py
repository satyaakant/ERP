from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from mitrr.models import (
    User, CustomSession, StudentList, TeacherList, Attendance, Subject, TimeTable, 
    Exam, Result, Notification,  Event,  AttendanceReport, Batch
)
from .serializers import (
    StudentSerializer, TeacherSerializer, 
    AttendanceSerializer, TimetableSerializer, ExamSerializer, ResultSerializer,
    NotificationSerializer, EventSerializer, 
    AttendanceReportSerializer, BatchSerializer
)


# StudentList views
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

@api_view(['DELETE'])
def deleteStudent_Mitrr(request, enroll_number):
    try:
        student = StudentList.objects.get(enroll_number=enroll_number)
        student.delete()
        return Response({"message": "Student deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except StudentList.DoesNotExist:
        return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

# TeacherList views
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
def deleteTeacher_Mitrr(request, teacher_id):
    try:
        teacher = TeacherList.objects.get(teacher_id=teacher_id)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except TeacherList.DoesNotExist:
        return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

# TimeTable views
@api_view(['POST'])
def addTimetable(request):
    serializer = TimetableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Timetable added successfully!"}, status=200)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def getTimetable(request):
    timeTable = TimeTable.objects.all()
    serializer = TimetableSerializer(timeTable, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Attendance views
@api_view(['GET'])
def getAttendanceList_Mitrr(request, year):
    enroll_number = request.query_params.get('enroll_number')
    month = request.query_params.get('month')
    subject_id = request.query_params.get('subject_id')
    section = request.query_params.get('section')
    semester = request.query_params.get('semester')

    if not enroll_number:
        return Response({"error": "Missing enroll_number in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = StudentList.objects.get(enroll_number=enroll_number, year=year)
    except StudentList.DoesNotExist:
        return Response({"error": f"Student with enrollment number {enroll_number} not found for year {year}."}, status=status.HTTP_404_NOT_FOUND)

    if subject_id:
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": f"Subject with ID {subject_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Missing subject_id in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
def getFilteredAttendanceList(request):
    year = request.query_params.get('year')
    subject_id = request.query_params.get('subject_id')
    section = request.query_params.get('section')
    semester = request.query_params.get('semester')

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

@api_view(['POST'])
def addAttendance(request):
    enroll_number = request.data.get('enroll_number')
    subject_id = request.data.get('subject_id')
    date = request.data.get('date')
    year = request.data.get('year')
    section = request.data.get('section')
    semester = request.data.get('semester')
    status_code = request.data.get('status', 'P')  # Default to 'Present' if not provided

    try:
        student = StudentList.objects.get(enroll_number=enroll_number)
    except StudentList.DoesNotExist:
        return Response({"error": f"Student with enrollment number {enroll_number} not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        return Response({"error": f"Subject with ID {subject_id} not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if Attendance.objects.filter(student=student, subject=subject, date=parsed_date).exists():
        return Response({"error": "Attendance record already exists for this student, subject, and date."}, status=status.HTTP_400_BAD_REQUEST)

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

# Exam views
@api_view(['GET'])
def getExamList(request):
    exams = Exam.objects.all()
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addExam(request):
    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Exam added successfully!"    }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def deleteExam(request, exam_id):
    try:
        exam = Exam.objects.get(pk=exam_id)
        exam.delete()
        return Response({"message": "Exam deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Exam.DoesNotExist:
        return Response({"error": "Exam not found."}, status=status.HTTP_404_NOT_FOUND)


# Result views
@api_view(['GET'])
def getResultList(request):
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addResult(request):
    serializer = ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Result added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def deleteResult(request, result_id):
    try:
        result = Result.objects.get(pk=result_id)
        result.delete()
        return Response({"message": "Result deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Result.DoesNotExist:
        return Response({"error": "Result not found."}, status=status.HTTP_404_NOT_FOUND)
# Notification views
@api_view(['GET'])
def getNotificationList(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addNotification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Notification added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteNotification(request, notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
        notification.delete()
        return Response({"message": "Notification deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

# Event views
@api_view(['GET'])
def getEventList(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addEvent(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Event added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteEvent(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return Response({"message": "Event deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

# AttendanceReport views
@api_view(['GET'])
def getAttendanceReportList(request):
    reports = AttendanceReport.objects.all()
    serializer = AttendanceReportSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addAttendanceReport(request):
    serializer = AttendanceReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Attendance report added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteAttendanceReport(request, report_id):
    try:
        report = AttendanceReport.objects.get(pk=report_id)
        report.delete()
        return Response({"message": "Attendance report deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except AttendanceReport.DoesNotExist:
        return Response({"error": "Attendance report not found."}, status=status.HTTP_404_NOT_FOUND)

# Batch views
@api_view(['GET'])
def getBatchList(request):
    batches = Batch.objects.all()
    serializer = BatchSerializer(batches, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addBatch(request):
    serializer = BatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Batch added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBatch(request, batch_id):
    try:
        batch = Batch.objects.get(pk=batch_id)
        batch.delete()
        return Response({"message": "Batch deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Batch.DoesNotExist:
        return Response({"error": "Batch not found."}, status=status.HTTP_404_NOT_FOUND)