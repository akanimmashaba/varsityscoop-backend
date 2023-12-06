from rest_framework import serializers
from taggit.serializers import (TaggitSerializer, TagListSerializerField)
from .models import Article, Category




class ArticleCreationSerializer(serializers.ModelSerializer, TaggitSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['slug']
    

class ArticleSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'title',
        ]



