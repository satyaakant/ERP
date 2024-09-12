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
    AttendanceReportSerializer, BatchSerializer, SubjectSerializer
)

@api_view(['GET'])
def getSubjectsBySemester(request):
    semester = request.query_params.get('semester')
    
    if semester is None:
        return Response({"error": "Semester is required"}, status=400)

    subjects = Subject.objects.filter(semester=semester)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)
# StudentList Views
@api_view(['GET'])
def getStudentList_Mitrr(request):
    batch = request.query_params.get('batch')
    section = request.query_params.get('section')

    if batch and section:
        students = StudentList.objects.filter(batch=batch, section=section)
    elif batch:
        students = StudentList.objects.filter(batch=batch)
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


# TeacherList Views
@api_view(['GET'])
def getTeacherList_Mitrr(request):
    teachers = TeacherList.objects.all()
    teacher_data = []
    for teacher in teachers:
        subjects = Subject.objects.filter(teacher=teacher)
        subjects_data = [{"name": subject.name, "code": subject.code, "semester": subject.semester} for subject in subjects]
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


# Attendance Views
@api_view(['GET'])
def getAttendanceList_Mitrr(request):
    # Fetch all attendance records
    attendance = Attendance.objects.all()

    if not attendance.exists():
        return Response({"error": "No attendance records found."}, status=status.HTTP_404_NOT_FOUND)

    # Construct the desired output structure
    response_data = {
        "course": "BTech",
        "batches": []
    }

    # Organize attendance records by batches and semesters
    batch_dict = {}
    for record in attendance:
        # Handle the case where the student's batch is None
        if record.student.batch:
            batch_name = f"Batch {record.student.batch.batch_name}"
        else:
            batch_name = "Unknown Batch"  # Default name for students without a batch

        semester_name = f"Sem{record.semester}"

        # Initialize batch and semester structure if not exists
        if batch_name not in batch_dict:
            batch_dict[batch_name] = {
                "name": batch_name,
                "semesters": {}
            }
        
        if semester_name not in batch_dict[batch_name]["semesters"]:
            batch_dict[batch_name]["semesters"][semester_name] = {
                "semester": semester_name,
                "subjects": {}
            }

        # Initialize subject structure
        if record.subject.name not in batch_dict[batch_name]["semesters"][semester_name]["subjects"]:
            batch_dict[batch_name]["semesters"][semester_name]["subjects"][record.subject.name] = {
                "name": record.subject.name,
                "temp_attendance": []
            }

        # Append attendance details
        batch_dict[batch_name]["semesters"][semester_name]["subjects"][record.subject.name]["temp_attendance"].append({
            "date": record.date.strftime("%Y-%m-%d"),
            "list": [
                {
                    "enrollNo": record.student.enroll_number,
                    "name": record.student.name,
                    "section": record.section,
                    "status": record.status.lower()  # Convert status to lowercase
                }
            ]
        })

    # Format the data in the required structure
    for batch_name, batch_data in batch_dict.items():
        semesters = []
        for semester_name, semester_data in batch_data["semesters"].items():
            subjects = []
            for subject_name, subject_data in semester_data["subjects"].items():
                subjects.append(subject_data)
            semester_data["subjects"] = subjects
            semesters.append(semester_data)
        batch_data["semesters"] = semesters
        response_data["batches"].append(batch_data)

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addAttendance(request):
    data = request.data.get('batches', [])
    
    if not data:
        return Response({"error": "Missing batches data"}, status=status.HTTP_400_BAD_REQUEST)
    
    for batch in data:
        batch_name = batch.get('name')
        semesters = batch.get('semesters', [])
        
        for semester in semesters:
            semester_number = semester.get('semester')[-1]
            subjects = semester.get('subjects', [])
            
            for subject_data in subjects:
                subject_name = subject_data.get('name')
                
                try:
                    subject = Subject.objects.get(name=subject_name, semester=semester_number)
                except Subject.DoesNotExist:
                    return Response({"error": f"Subject {subject_name} not found for semester {semester_number}"}, status=status.HTTP_404_NOT_FOUND)
                
                temp_attendance = subject_data.get('temp_attendance', [])
                
                for attendance_data in temp_attendance:
                    attendance_date = attendance_data.get('date')
                    students_list = attendance_data.get('list', [])
                    
                    try:
                        parsed_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()
                    except ValueError:
                        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    for student_data in students_list:
                        enroll_no = student_data.get('enrollNo')
                        status_code = student_data.get('status', 'P').upper()
                        section = student_data.get('section')

                        try:
                            student = StudentList.objects.get(enroll_number=enroll_no)
                        except StudentList.DoesNotExist:
                            return Response({"error": f"Student with enrollment number {enroll_no} not found."}, status=status.HTTP_404_NOT_FOUND)

                        # Save or update the attendance record
                        attendance, created = Attendance.objects.update_or_create(
                            student=student,
                            subject=subject,
                            date=parsed_date,
                            defaults={'status': status_code, 'section': section, 'semester': semester_number}
                        )

    return Response({"message": "Attendance added successfully!"}, status=status.HTTP_201_CREATED)


# Timetable Views
@api_view(['POST'])
def addTimetable(request):
    serializer = TimetableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Timetable added successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getTimetable(request):
    timetables = TimeTable.objects.all()
    serializer = TimetableSerializer(timetables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Exam Views
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
        return Response({"message": "Exam added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteExam(request, exam_id):
    try:
        exam = Exam.objects.get(pk=exam_id)
        exam.delete()
        return Response({"message": "Exam deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Exam.DoesNotExist:
        return Response({"error": "Exam not found."}, status=status.HTTP_404_NOT_FOUND)


# Result Views
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


# Notification Views
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


# Event Views
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


# AttendanceReport Views
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


# Batch Views
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
