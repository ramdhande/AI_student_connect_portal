from django.shortcuts import redirect, get_object_or_404
from .models import Grievance, Notification
from ai_module.sentiment import analyze_sentiment, determine_priority
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def submit_grievance(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        
        sentiment = analyze_sentiment(description)
        priority = determine_priority(description, sentiment)
        
        Grievance.objects.create(
            student=request.user,
            subject=subject,
            description=description,
            sentiment=sentiment,
            priority=priority
        )
    return redirect('/dashboard/')


@login_required(login_url='/login/')
def update_grievance_status(request, grievance_id):
    if request.user.role != 'admin':
        return redirect('/dashboard/')
        
    if request.method == "POST":
        status = request.POST.get('status')
        admin_message = request.POST.get('admin_message', '')
        
        grievance = get_object_or_404(Grievance, id=grievance_id)
        grievance.status = status
        grievance.admin_message = admin_message
        grievance.save()
        
        # Create a notification for the student
        Notification.objects.create(
            recipient=grievance.student,
            message=f"Status update: Your complaint '{grievance.subject}' is now marked as {status.replace('_', ' ').title()}.",
            notification_type='grievance'
        )
        
    return redirect('/admin-dashboard/')
