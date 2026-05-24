from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notice
from grievances.models import Grievance, Notification
from accounts.models import User, StudentProfile
from ai_module.translation import translate_text

@login_required(login_url='/login/')
def student_dashboard(request):
    # Role checking: admins should go to the admin dashboard
    if request.user.role == 'admin':
        return redirect('/admin-dashboard/')
        
    notices = Notice.objects.all().order_by('-priority', '-created_at')
    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    
    # Mark user's notifications as read or fetch unread ones
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    
    # Optional: Mark them as read on load
    # notifications.update(is_read=True)
    
    return render(request, 'student_dashboard.html', {
        'notices': notices, 
        'grievances': grievances,
        'notifications': notifications
    })

@login_required(login_url='/login/')
def admin_dashboard(request):
    if request.user.role != 'admin':
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
    if request.user.role != 'admin':
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