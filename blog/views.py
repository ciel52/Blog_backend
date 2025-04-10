from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets,filters,permissions,generics
from .serializers import PostSerializer
from .models import Post
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class IndexView(TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = 'blog/index.html'


class PostListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()