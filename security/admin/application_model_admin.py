from django.contrib import admin
from security.models import ApplicationModel


class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'user', 'is_staff', 'is_enabled', 'created', 'modified')
    search_fields = ('name', 'code', 'user__username')
    list_filter = ('is_staff', 'is_enabled', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': (
            'name', 'code', 'user', 'key', 'secret', 'two_factor_enabled', 'is_staff', 'is_enabled', 'parent', 'logo',
            'about')
        }),
        ('Audit Info', {
            'fields': ('created', 'created_by', 'modified', 'modified_by'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(ApplicationModel, ApplicationModelAdmin)
