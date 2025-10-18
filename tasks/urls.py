from django.urls import include, path
from rest_framework import routers
from tasks import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskView, 'tasks')
router.register(r'categories', views.CategoryView, 'categories')

urlpatterns = [
    path("api/v1/", include(router.urls))
]