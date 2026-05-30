from django.contrib import admin
from scanner.models import ScanResult

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['resume_filename', 'match_score', 'created_at']
    list_filter = ['match_score']
    ordering = ['-created_at']