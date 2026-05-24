from django.urls import path
from .views import student_dashboard, admin_dashboard, create_notice, translate_notice

app_name = 'notices'

urlpatterns = [
    path('dashboard/', student_dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('notices/create/', create_notice, name='create_notice'),
    path('notices/translate/', translate_notice, name='translate_notice'),
]
