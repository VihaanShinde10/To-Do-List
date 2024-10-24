from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'complete', 'created')
    list_filter = ('complete', 'created', 'user')
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)
