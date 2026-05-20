from django.contrib import admin
from .models import Grievance

@admin.action(description="Mark selected grievances as Resolved")
def mark_resolved(modeladmin, request, queryset):
    queryset.update(status='resolved')

class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'status', 'sentiment', 'created_at')
    list_filter = ('status', 'sentiment')
    actions = [mark_resolved]

admin.site.register(Grievance, GrievanceAdmin)
