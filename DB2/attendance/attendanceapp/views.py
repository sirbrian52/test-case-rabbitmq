from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from .models import employee
from .serializer import AttendanceSerializer
from celery.result import AsyncResult
from django.conf import settings


@api_view(['POST'])
def receive_data(request):
    serializer = AttendanceSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Success case
        except IntegrityError as e:
            return Response({'status': 'Error', 'message': 'Database integrity error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'Validation Error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)  # Validation failure



@api_view(['GET'])
def list_attendance(request):
    attendance_records = employee.objects.all()
    serializer = AttendanceSerializer(attendance_records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



def check_task(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return {'status':200,'task':'found','result':result.result}
    else:
        return {'status':404,'task':'not found','result':result.result}