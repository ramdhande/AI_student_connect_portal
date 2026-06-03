from django.http import JsonResponse
from .chatbot import chatbot_reply

def chatbot_response(request):
    user = request.user

    # Allow unauthenticated guest users, but if logged in, enforce standard role validation
    if user.is_authenticated and user.role not in ['student', 'parent', 'admin', 'teacher']:
        return JsonResponse({'reply': 'Please login with a valid role to use the chatbot.'})

    message = request.GET.get('message', '')
    reply = chatbot_reply(message)

    return JsonResponse({'reply': reply})


def suggest_notice_category(request):
    title = request.GET.get('title', '')
    content = request.GET.get('content', '')
    
    text = (title + " " + content).lower()
    
    if any(kw in text for kw in ["exam", "schedule", "midterm", "result", "grade", "marks", "academic", "syllabus", "timetable", "test"]):
        category = "Academic"
    elif any(kw in text for kw in ["placement", "job", "hiring", "recruitment", "drive", "interview", "careers", "wipro", "tcs", "cognizant"]):
        category = "Placement"
    elif any(kw in text for kw in ["fest", "sports", "holiday", "gather", "event", "cultural", "celebrate", "annual", "club", "workshop"]):
        category = "Events"
    elif any(kw in text for kw in ["urgent", "immediate", "caution", "fire", "alert", "block", "weather", "flood", "closed", "emergency"]):
        category = "Emergency"
    else:
        category = "Administrative"
        
    return JsonResponse({'category': category})
