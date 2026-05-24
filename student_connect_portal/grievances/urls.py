from django.urls import path
from .views import submit_grievance, update_grievance_status

app_name = 'grievances'

urlpatterns = [
    path('submit/', submit_grievance, name='submit'),
    path('update-status/<int:grievance_id>/', update_grievance_status, name='update_status'),
]
