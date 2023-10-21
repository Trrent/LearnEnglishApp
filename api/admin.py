from django.contrib import admin
from api.models import User
from django.contrib.auth.admin import UserAdmin
from api.forms import CustomUserAddForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAddForm
    form = CustomUserChangeForm
    list_display = ('id', 'username', 'email')
    list_filter = ('is_admin', 'is_active', 'is_superuser', 'is_staff')
    readonly_fields = ['created_at', 'uuid']
    search_fields = ('id', 'uuid', 'username', 'email')
    ordering = ('id', )
    fieldsets = (
        ('User', {'fields': ('uuid', 'username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_admin', 'is_staff')}),
        ('Dates', {'fields': ('created_at',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'confirm_password'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)