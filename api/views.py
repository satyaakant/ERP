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
