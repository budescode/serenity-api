from django.contrib import admin
from .models import CustomUser, PasswordCode


class CustomUserAdmin(admin.ModelAdmin):
	list_display = ['username', 'email', 'fullname']

class PasswordCodeAdmin(admin.ModelAdmin):
	list_display = ['email', 'code']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordCode, PasswordCodeAdmin)