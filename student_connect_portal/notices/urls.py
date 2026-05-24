from django.urls import path
from .views import (
    student_dashboard,
    student_dashboard_home,
    student_dashboard_timetable,
    student_dashboard_grievances,
    student_dashboard_notices,
    student_dashboard_examination,
    student_dashboard_reference,
    parent_dashboard_home,
    parent_dashboard_timetable,
    parent_dashboard_grievances,
    parent_dashboard_notices,
    parent_dashboard_examination,
    parent_link_child,
    admin_dashboard,
    create_notice,
    translate_notice,
)

app_name = 'notices'

urlpatterns = [
    # Student Dashboard Pages
    path('dashboard/', student_dashboard, name='dashboard'),
    path('dashboard/home/', student_dashboard_home, name='dashboard_home'),
    path('dashboard/timetable/', student_dashboard_timetable, name='dashboard_timetable'),
    path('dashboard/grievances/', student_dashboard_grievances, name='dashboard_grievances'),
    path('dashboard/notices/', student_dashboard_notices, name='dashboard_notices'),
    path('dashboard/examination/', student_dashboard_examination, name='dashboard_examination'),
    path('dashboard/reference/', student_dashboard_reference, name='dashboard_reference'),
    
    # Parent Dashboard Pages
    path('parent/dashboard/', parent_dashboard_home, name='parent_dashboard'),
    path('parent/dashboard/home/', parent_dashboard_home, name='parent_dashboard_home'),
    path('parent/dashboard/timetable/', parent_dashboard_timetable, name='parent_dashboard_timetable'),
    path('parent/dashboard/grievances/', parent_dashboard_grievances, name='parent_dashboard_grievances'),
    path('parent/dashboard/notices/', parent_dashboard_notices, name='parent_dashboard_notices'),
    path('parent/dashboard/examination/', parent_dashboard_examination, name='parent_dashboard_examination'),
    path('parent/dashboard/link-child/', parent_link_child, name='parent_link_child'),
    
    # Admin Pages
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('notices/create/', create_notice, name='create_notice'),
    path('notices/translate/', translate_notice, name='translate_notice'),
]
