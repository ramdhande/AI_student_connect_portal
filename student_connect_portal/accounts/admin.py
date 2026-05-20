from django.contrib import admin
from .models import User
from .models import StudentProfile

admin.site.register(StudentProfile)

admin.site.register(User)
