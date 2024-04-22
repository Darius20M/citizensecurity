from django.contrib import admin
from django.contrib.auth.models import User

from security.models import SessionModel


class SessionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'application', 'ip_address', 'expire', 'offline', 'last_activity')
    list_filter = ('application', 'offline', 'last_activity')
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['created', 'modified', 'last_offline', 'time_no_ready', 'fullname']

    def fullname(self, obj):
        return obj.fullname()

    fullname.short_description = 'Full Name'
    fullname.admin_order_field = 'user__first_name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'application')
        return queryset

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo los superusuarios pueden cambiar

    def has_add_permission(self, request):
        return request.user.is_superuser  # Solo los superusuarios pueden cambiar


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo los superusuarios pueden cambiar

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(SessionModel, SessionModelAdmin)
