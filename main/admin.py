from django.contrib import admin

from .models import List, Task, Invitation

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create')
    list_display_links = ('id', 'title')
    filter_horizontal = ('participants',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'time_create', 'time_update', 'is_completed')

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'list','time_create', 'status']
