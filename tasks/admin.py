from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'task_count', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at']

    def task_count(self, obj):
        return obj.task_set.count()

    task_count.short_description = 'Número de Tareas'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'done', 'is_overdue_status', 'due_date', 'created_at']
    list_filter = ['done', 'category', 'priority', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'is_overdue']

    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description', 'done')
        }),
        ('Clasificación', {
            'fields': ('category', 'priority')
        }),
        ('Fechas', {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
        ('Estado', {
            'fields': ('is_overdue',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    def is_overdue_status(self, obj):
        if obj.is_overdue:
            return 'VENCIDA'
        return 'AL DIA'

    is_overdue_status.short_description = 'Estado'