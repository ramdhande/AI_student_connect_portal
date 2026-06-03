from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notice
from grievances.models import Grievance, Notification
from accounts.models import User, StudentProfile, TeacherProfile, ParentProfile, StudentProgress, Attendance
from ai_module.translation import translate_text


@login_required(login_url='/login/')
def student_dashboard(request):
    return redirect('/dashboard/home/')

@login_required(login_url='/login/')
def student_dashboard_home(request):
    if request.user.role == 'admin':
        return redirect('/admin-dashboard/')
    elif request.user.role == 'parent':
        return redirect('/parent/dashboard/home/')
        
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    
    return render(request, 'student/home.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def student_dashboard_timetable(request):
    if request.user.role != 'student':
        return redirect('/login/')
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'student/timetable.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def student_dashboard_grievances(request):
    if request.user.role != 'student':
        return redirect('/login/')
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'student/grievances.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def student_dashboard_notices(request):
    if request.user.role != 'student':
        return redirect('/login/')
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'student/notices.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def student_dashboard_examination(request):
    if request.user.role != 'student':
        return redirect('/login/')
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'student/examination.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def student_dashboard_reference(request):
    if request.user.role != 'student':
        return redirect('/login/')
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'student_dashboard_reference.html', {
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def parent_dashboard_home(request):
    if request.user.role != 'parent':
        return redirect('/login/')
        
    student_id = request.session.get('linked_student_id')
    if not student_id:
        return redirect('/parent/dashboard/link-child/')
        
    child_profile = get_object_or_404(StudentProfile, student_id=student_id)
    child_user = User.objects.filter(student_profile=child_profile).first()
    
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    
    if child_user:
        grievances = Grievance.objects.filter(student=child_user).order_by('-created_at')
        notifications = Notification.objects.filter(recipient=child_user, is_read=False).order_by('-created_at')
    else:
        grievances = Grievance.objects.none()
        notifications = Notification.objects.none()
        
    # Calculate overall attendance average
    att_list = Attendance.objects.filter(student=child_profile)
    overall_attendance = int(sum(a.percentage for a in att_list) / att_list.count()) if att_list.exists() else 0
        
    return render(request, 'parent/home.html', {
        'child_profile': child_profile,
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications,
        'overall_attendance': overall_attendance
    })

@login_required(login_url='/login/')
def parent_dashboard_timetable(request):
    if request.user.role != 'parent':
        return redirect('/login/')
        
    student_id = request.session.get('linked_student_id')
    if not student_id:
        return redirect('/parent/dashboard/link-child/')
        
    child_profile = get_object_or_404(StudentProfile, student_id=student_id)
    child_user = User.objects.filter(student_profile=child_profile).first()
    
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    if child_user:
        grievances = Grievance.objects.filter(student=child_user).order_by('-created_at')
        notifications = Notification.objects.filter(recipient=child_user, is_read=False).order_by('-created_at')
    else:
        grievances = Grievance.objects.none()
        notifications = Notification.objects.none()
        
    return render(request, 'parent/timetable.html', {
        'child_profile': child_profile,
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def parent_dashboard_grievances(request):
    # Grievances are kept private to the student and are not accessible by parents.
    return redirect('/parent/dashboard/home/')

@login_required(login_url='/login/')
def parent_dashboard_notices(request):
    if request.user.role != 'parent':
        return redirect('/login/')
        
    student_id = request.session.get('linked_student_id')
    if not student_id:
        return redirect('/parent/dashboard/link-child/')
        
    child_profile = get_object_or_404(StudentProfile, student_id=student_id)
    child_user = User.objects.filter(student_profile=child_profile).first()
    
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    if child_user:
        grievances = Grievance.objects.filter(student=child_user).order_by('-created_at')
        notifications = Notification.objects.filter(recipient=child_user, is_read=False).order_by('-created_at')
    else:
        grievances = Grievance.objects.none()
        notifications = Notification.objects.none()
        
    return render(request, 'parent/notices.html', {
        'child_profile': child_profile,
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def parent_dashboard_examination(request):
    if request.user.role != 'parent':
        return redirect('/login/')
        
    student_id = request.session.get('linked_student_id')
    if not student_id:
        return redirect('/parent/dashboard/link-child/')
        
    child_profile = get_object_or_404(StudentProfile, student_id=student_id)
    child_user = User.objects.filter(student_profile=child_profile).first()
    
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    if child_user:
        grievances = Grievance.objects.filter(student=child_user).order_by('-created_at')
        notifications = Notification.objects.filter(recipient=child_user, is_read=False).order_by('-created_at')
    else:
        grievances = Grievance.objects.none()
        notifications = Notification.objects.none()
        
    return render(request, 'parent/examination.html', {
        'child_profile': child_profile,
        'notices': notices,
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def parent_link_child(request):
    if request.user.role != 'parent':
        return redirect('/login/')
        
    if request.method == "POST":
        student_id = request.POST.get('student_id', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        
        # Verify in StudentProfile
        profile = StudentProfile.objects.filter(student_id=student_id, full_name__iexact=full_name).first()
        if profile:
            request.session['linked_student_id'] = profile.student_id
            return redirect('/parent/dashboard/home/')
        else:
            return render(request, 'parent/link_child.html', {
                'error': 'Child profile verification failed. Check ID or Full Name.'
            })
            
    return render(request, 'parent/link_child.html')

@login_required(login_url='/login/')
def admin_dashboard(request):
    if request.user.role not in ['admin', 'teacher']:
        return redirect('/dashboard/')
        
    notices = Notice.objects.all().order_by('-created_at')
    grievances = Grievance.objects.all().order_by('-created_at')
    
    # Metrics calculations
    total_students = User.objects.filter(role='student').count()
    total_notices = notices.count()
    total_grievances = grievances.count()
    
    pending_grievances = grievances.filter(status='pending').count()
    inprogress_grievances = grievances.filter(status='in_progress').count()
    resolved_grievances = grievances.filter(status='resolved').count()
    
    sentiment_pos = grievances.filter(sentiment='Positive').count()
    sentiment_neg = grievances.filter(sentiment='Negative').count()
    sentiment_neu = grievances.filter(sentiment='Neutral').count()
    
    return render(request, 'admin_dashboard.html', {
        'notices': notices,
        'grievances': grievances,
        'total_students': total_students,
        'total_notices': total_notices,
        'total_grievances': total_grievances,
        'pending_grievances': pending_grievances,
        'inprogress_grievances': inprogress_grievances,
        'resolved_grievances': resolved_grievances,
        'sentiment_pos': sentiment_pos,
        'sentiment_neg': sentiment_neg,
        'sentiment_neu': sentiment_neu,
    })

@login_required(login_url='/login/')
def create_notice(request):
    if request.user.role not in ['admin', 'teacher']:
        return redirect('/dashboard/')
        
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        priority = int(request.POST.get('priority', 0))
        
        notice = Notice.objects.create(
            title=title,
            content=content,
            category=category,
            priority=priority,
            created_by=request.user
        )
        
        # Broadcast notice notification to all students
        students = User.objects.filter(role='student')
        for s in students:
            Notification.objects.create(
                recipient=s,
                message=f"New Announcement: {title} ({category})",
                notification_type='notice'
            )
            
    return redirect('/admin-dashboard/')

@login_required(login_url='/login/')
def translate_notice(request):
    notice_id = request.GET.get('notice_id')
    lang = request.GET.get('lang', 'hindi')
    
    notice = get_object_or_404(Notice, id=notice_id)
    
    translated_title = translate_text(notice.title, lang)
    translated_content = translate_text(notice.content, lang)
    
    return JsonResponse({
        'translated_title': translated_title,
        'translated_content': translated_content,
        'lang': lang.capitalize()
    })


@login_required(login_url='/login/')
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('/login/')
        
    students = StudentProfile.objects.all()
    notices = Notice.objects.all().order_by('-created_at')
    grievances = Grievance.objects.all().order_by('-created_at')
    
    # Calculate some dashboard metrics
    total_students = StudentProfile.objects.count()
    total_notices = notices.count()
    total_grievances = grievances.count()
    
    pending_grievances = grievances.filter(status='pending').count()
    inprogress_grievances = grievances.filter(status='in_progress').count()
    resolved_grievances = grievances.filter(status='resolved').count()
    
    # Compute grade distribution counts
    grades = StudentProgress.objects.all()
    grade_counts = {
        'A_plus': grades.filter(grade='A+').count(),
        'A': grades.filter(grade='A').count(),
        'B_plus': grades.filter(grade='B+').count(),
        'B': grades.filter(grade='B').count(),
        'C': grades.filter(grade='C').count(),
        'F': grades.filter(grade='F').count(),
    }

    # Compute attendance thresholds
    att_records = Attendance.objects.all()
    att_above = att_records.filter(percentage__gte=75).count()
    att_below = att_records.filter(percentage__lt=75).count()
    
    return render(request, 'teacher_dashboard.html', {
        'students': students,
        'notices': notices,
        'grievances': grievances,
        'total_students': total_students,
        'total_notices': total_notices,
        'total_grievances': total_grievances,
        'pending_grievances': pending_grievances,
        'inprogress_grievances': inprogress_grievances,
        'resolved_grievances': resolved_grievances,
        'grade_counts': grade_counts,
        'att_above': att_above,
        'att_below': att_below,
    })


@login_required(login_url='/login/')
def teacher_add_student(request):
    if request.user.role != 'teacher':
        return redirect('/login/')
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        year = int(request.POST.get('year', 1))
        
        StudentProfile.objects.create(
            student_id=student_id,
            full_name=full_name,
            email=email,
            department=department,
            year=year
        )
    return redirect('/teacher/dashboard/')


@login_required(login_url='/login/')
def teacher_update_metrics(request):
    if request.user.role != 'teacher':
        return redirect('/login/')
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        metric_type = request.POST.get('metric_type') # 'progress' or 'attendance'
        
        student = get_object_or_404(StudentProfile, student_id=student_id)
        
        if metric_type == 'progress':
            marks = int(request.POST.get('marks', 0))
            grade = request.POST.get('grade', 'F')
            semester = int(request.POST.get('semester', 1))
            
            StudentProgress.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': marks, 'grade': grade, 'semester': semester}
            )
        elif metric_type == 'attendance':
            percentage = int(request.POST.get('percentage', 0))
            total_classes = int(request.POST.get('total_classes', 40))
            classes_attended = int(request.POST.get('classes_attended', 0))
            
            Attendance.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'percentage': percentage, 'total_classes': total_classes, 'classes_attended': classes_attended}
            )
            
    return redirect('/teacher/dashboard/')