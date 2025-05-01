from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from .serializers import UserPostSerializer, AdminPostSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class IndexView(TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = 'blog/index.html'


# ユーザー用のView
class UserPostViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    ユーザー向けの投稿一覧・詳細取得用ViewSet
    ListModelMixin: 一覧取得
    RetrieveModelMixin: 詳細取得
    """
    serializer_class = UserPostSerializer
    queryset = Post.objects.all()


# 管理者用のView
class AdminPostViewSet(viewsets.ModelViewSet):
    """
    管理者向けの投稿管理用ViewSet
    ModelViewSet: 一覧・作成・詳細・更新・削除の全機能を提供
    """
    serializer_class = AdminPostSerializer
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"管理者による投稿作成: {request.user.username}")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"投稿作成エラー: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            logger.info(f"管理者による投稿更新: {request.user.username}")
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"投稿更新エラー: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    def partial_update(self, request, *args, **kwargs):
        try:
            logger.info(f"管理者による投稿部分更新: {request.user.username}")
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"投稿部分更新エラー: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
