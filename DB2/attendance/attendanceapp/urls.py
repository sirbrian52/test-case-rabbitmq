from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.list_attendance, name='list_attendance'),
    path('receive-data/', views.receive_data, name='receive_data'),
]
