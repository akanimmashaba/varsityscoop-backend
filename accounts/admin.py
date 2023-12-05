from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type','is_superuser','is_regular','is_staff','is_admin', 'is_active',)
    list_filter = ('is_superuser', 'is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),
        ('groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_admin','is_superuser', 'is_active')}),
    )
    
    inlines = (UserProfileInline,)
    search_fields = ('email', 'username',)
    ordering = ('email',)


class AbstractGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


admin.site.register(Account, CustomUserAdmin)
admin.site.register(Profile)