from djoser.serializers import UserSerializer
from articles.serializers import ArticleSerializer

class CustomUserSerializer(UserSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('articles',)