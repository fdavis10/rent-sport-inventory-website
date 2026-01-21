from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_full_name_display', 'role', 'is_staff', 'is_superuser', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'avatar')
        }),
        ('Роль и права', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
            'description': 'is_staff и is_superuser устанавливаются автоматически на основе роли'
        }),
        ('Группы и права доступа', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'phone_number', 'address', 'date_of_birth')
        }),
        ('Роль', {
            'fields': ('role',),
            'description': 'Роль автоматически установит is_staff и is_superuser'
        }),
    )
    
    def get_full_name_display(self, obj):
        return obj.get_full_name() or '-'
    get_full_name_display.short_description = 'Полное имя'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        self.message_user(
            request,
            f'Пользователь {obj.username} сохранён с ролью {obj.get_role_display()} '
            f'(is_staff={obj.is_staff}, is_superuser={obj.is_superuser})'
        )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.role == User.Role.MANAGER:
            return qs.filter(role=User.Role.CLIENT)
        
        return qs
    
    def has_delete_permission(self, request, obj=None):
        if request.user.role == User.Role.MANAGER:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.role == User.Role.MANAGER and obj:
            if obj.role in [User.Role.MANAGER, User.Role.ADMIN]:
                return False
        return super().has_change_permission(request, obj)