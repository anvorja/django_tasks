from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import TaskSerializer, CategorySerializer
from .models import Task, Category


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['done', 'category', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'title']
    ordering = ['-created_at']

    @action(detail=True, methods=['patch'])
    def toggle_done(self, request, pk=None):
        """Toggle the done status of a task"""
        task = self.get_object()
        task.done = not task.done
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get task statistics"""
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(done=True).count()
        pending_tasks = total_tasks - completed_tasks

        # Calcular tareas vencidas
        overdue_tasks = 0
        for task in Task.objects.filter(done=False):
            if task.is_overdue:
                overdue_tasks += 1

        # Estadísticas por categoría
        category_stats = []
        for category in Category.objects.all():
            cat_tasks = Task.objects.filter(category=category)
            category_stats.append({
                'category': category.name,
                'color': category.color,
                'total': cat_tasks.count(),
                'completed': cat_tasks.filter(done=True).count(),
                'pending': cat_tasks.filter(done=False).count()
            })

        return Response({
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'overdue': overdue_tasks,
            'by_category': category_stats
        })