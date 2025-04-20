from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admin/posts', views.AdminPostViewSet)
router.register(r'posts', views.UserPostViewSet, basename='user-post')

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]