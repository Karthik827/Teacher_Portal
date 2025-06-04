from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student

class TeacherAdmin(UserAdmin):
    """
    Custom admin interface for the Teacher model.

    Configures list display, filters, search, and fieldsets for managing teacher records.
    """
    model = Teacher
    list_display = ('username', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student)