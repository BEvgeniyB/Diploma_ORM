from django.contrib import admin
from .models import User,Task

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)