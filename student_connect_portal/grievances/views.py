from django.shortcuts import redirect
from .models import Grievance
from ai_module.sentiment import analyze_sentiment
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def submit_grievance(request):
    if request.method == "POST":
        sentiment = analyze_sentiment(request.POST['description'])
        Grievance.objects.create(
            student=request.user,
            subject=request.POST['subject'],
            description=request.POST['description'],
            sentiment=sentiment
        )
    return redirect('/dashboard/')
