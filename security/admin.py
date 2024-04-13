from django.contrib import admin
from .models import ApplicationModel

@admin.register(ApplicationModel)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_2fa', 'is_staff', 'is_enabled', 'created', 'modified']
    search_fields = ['name', 'user__username']
    list_filter = ['is_2fa', 'is_staff', 'is_enabled', 'created', 'modified']
    readonly_fields = ['key', 'secret', 'created', 'modified']
