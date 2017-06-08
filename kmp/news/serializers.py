from rest_framework.serializers import ModelSerializer, ListSerializer
from news.models import Article, Keyphrase


class KeyphraseSerializer(ModelSerializer):
    class Meta:
        model = Keyphrase
        fields = (
            'text',
            'score',
        )

class ArticleSerializer(ModelSerializer):
    keyphrases = KeyphraseSerializer(many=True)
    class Meta:
        model = Article
        fields = (
            'title',
            'keyphrases',
        )
