from django.urls import path
from .views import (
    login_view, signup_view, logout_view,
    student_login_view, student_signup_view,
    teacher_login_view, teacher_signup_view,
    parent_login_view, parent_signup_view
)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    
    path('student/login/', student_login_view, name='student_login'),
    path('student/signup/', student_signup_view, name='student_signup'),
    
    path('teacher/login/', teacher_login_view, name='teacher_login'),
    path('teacher/signup/', teacher_signup_view, name='teacher_signup'),
    
    path('parent/login/', parent_login_view, name='parent_login'),
    path('parent/signup/', parent_signup_view, name='parent_signup'),
    
    path('logout/', logout_view, name='logout'),
]
