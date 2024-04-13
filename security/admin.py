from django.contrib import admin
from .models import ApplicationModel

@admin.register(ApplicationModel)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'two_factor_enabled', 'is_staff', 'is_enabled', 'created', 'modified']
    search_fields = ['name', 'user__username']
    list_filter = ['two_factor_enabled', 'is_staff', 'is_enabled', 'created', 'modified']
    readonly_fields = ['key', 'secret', 'created', 'modified']
