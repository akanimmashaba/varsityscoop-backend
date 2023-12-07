from rest_framework import viewsets
from .models import Article, Category
from .serializers import (
    ArticleCreationSerializer,
    ArticleSerializer,
    CategorySerializer,
    CategoryCreationSerializer,
)
from rest_framework import permissions
from rest_framework.response import Response
from djoser.permissions import CurrentUserOrAdminOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [CurrentUserOrAdminOrReadOnly]

    lookup_field = 'slug'
    # lookup_url_kwarg = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreationSerializer
        return ArticleSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = [CurrentUserOrAdminOrReadOnly]



    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreationSerializer
        return CategorySerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        articles_serializer = ArticleSerializer(instance.articles.all(), many=True)
        data = serializer.data
        data['articles'] = articles_serializer.data
        return Response(data)