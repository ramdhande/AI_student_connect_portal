from django.contrib import admin
admin.site.site_header = "AI Student Connect Portal – Administration"
admin.site.site_title = "AI Student Connect Portal Admin"
admin.site.index_title = "Welcome to AI Student Connect Portal Admin Dashboard"
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/login/')

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('', include('accounts.urls')),
    path('', include('notices.urls')),
    path('grievance/', include('grievances.urls')),
    path('chatbot/', include('ai_module.urls')),
    path('admin/', admin.site.urls),
]
