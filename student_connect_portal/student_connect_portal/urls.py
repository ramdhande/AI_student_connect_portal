from django.contrib import admin
admin.site.site_header = "AI Student Connect Portal – Administration"
admin.site.site_title = "AI Student Connect Portal Admin"
admin.site.index_title = "Welcome to AI Student Connect Portal Admin Dashboard"
from django.urls import path
from notices.views import student_dashboard
from grievances.views import submit_grievance
from ai_module.views import chatbot_response
from accounts.views import login_view, signup_view, logout_view
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/login/')


urlpatterns = [
    path('', home_redirect),
    path('login/', login_view),
    path('signup/', signup_view),
    path('logout/', logout_view),

    path('dashboard/', student_dashboard),
    path('grievance/submit/', submit_grievance),
    path('chatbot/', chatbot_response),

    path('admin/', admin.site.urls),
]
