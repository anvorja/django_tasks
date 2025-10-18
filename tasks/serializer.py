from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'created_at', 'task_count']

    def get_task_count(self, obj):
        return obj.task_set.count()


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'done', 'category',
            'category_name', 'category_color', 'priority',
            'due_date', 'created_at', 'updated_at', 'is_overdue'
        ]
        read_only_fields = ['created_at', 'updated_at']