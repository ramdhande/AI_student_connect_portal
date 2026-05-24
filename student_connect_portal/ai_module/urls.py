from django.urls import path
from .views import chatbot_response, suggest_notice_category

app_name = 'ai_module'

urlpatterns = [
    path('', chatbot_response, name='chatbot_response'),
    path('suggest-category/', suggest_notice_category, name='suggest_category'),
]
