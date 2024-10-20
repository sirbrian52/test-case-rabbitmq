from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from managemenapp.tasks import send_data_to_attendance  

@api_view(['POST'])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        employee_instance = serializer.save()

        data = {
            'name': employee_instance.name,
            'badge': employee_instance.badge,
            'email': employee_instance.email,
            'password': employee_instance.password,
        }

        send_data_to_attendance.delay(data)

        return Response({'status': 'Employee data successfully added and task sent to RabbitMQ.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
