from celery import shared_task
import requests
import logging
from django.db import transaction
from .models import Employee
from .serializers import EmployeeSerializer

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_data_to_attendance(self, data):
    logger.info(f'Sending data to RabbitMQ: {data}')
    
    try:
        response = requests.post('http://127.0.0.1:8081/api/receive-data/', json=data)
        response.raise_for_status()  

        with transaction.atomic():
            employee_serializer = EmployeeSerializer(data=data)
            if employee_serializer.is_valid():
                employee_serializer.save()
                logger.info('Employee data saved to database after successful RabbitMQ processing.')
            else:
                logger.error('Employee data is invalid: %s', employee_serializer.errors)
                raise ValueError('Invalid employee data.')

        return 'Employee data successfully sent and saved in the database.'

    except requests.exceptions.RequestException as exc:
        logger.error(f'Error sending data to RabbitMQ: {exc}')
        self.retry(exc=exc, countdown=10)  

    except Exception as e:
        logger.error(f'Error processing task: {e}')
        raise self.retry(exc=e, countdown=10)
