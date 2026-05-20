from django.http import JsonResponse
from .chatbot import chatbot_reply

def chatbot_response(request):
    user = request.user

    # Allow only logged-in users
    if not user.is_authenticated:
        return JsonResponse({'reply': 'Please login to use the chatbot.'})

    # Allow only Student or Parent roles
    if user.role not in ['student', 'parent','admin']:
        return JsonResponse({'reply': 'Please login with a valid role to use the chatbot.'})

    message = request.GET.get('message', '')
    reply = chatbot_reply(message)

    return JsonResponse({'reply': reply})
