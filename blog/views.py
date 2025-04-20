from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, filters, permissions, generics, mixins
from django.http import JsonResponse
from .serializers import UserPostSerializer, AdminPostSerializer
from .models import Post
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
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
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Received data: {request.data}")
            logger.info(f"Auth: {request.auth}")
            logger.info(f"User: {request.user}")
            logger.info(f"Headers: {request.headers}")
            logger.info(f"Is Admin: {request.user.is_staff}")
            logger.info(f"Is Superuser: {request.user.is_superuser}")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
