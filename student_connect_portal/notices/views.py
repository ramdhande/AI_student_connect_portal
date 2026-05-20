from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notice
from grievances.models import Grievance

@login_required(login_url='/login/')
def student_dashboard(request):
    notices = Notice.objects.all().order_by('-priority')
    grievances = Grievance.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'notices': notices, 'grievances': grievances})