

from rest_framework.serializers import ModelSerializer, ListSerializer, SerializerMethodField
from news.models import Article, Keyphrase, Photo
import os


class KeyphraseSerializer(ModelSerializer):
    class Meta:
        model = Keyphrase
        fields = (
            'text',
            'score',
        )

class ArticleListSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'description',
            'url',
        )

class ArticleSerializer(ModelSerializer):
    keyphrases = KeyphraseSerializer(many=True)
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'keyphrases',
        )


class PhotoSerializer(ModelSerializer):

    image = SerializerMethodField()

    class Meta:
        model = Photo
        fields = ("image",)

    #Serializer method field to change output of the image path
    def get_image(self, obj):
        print("GET IMAGE: ", obj)
        #must refactor to use static folder
        return os.path.basename(obj.image.name)


class ArticlePhotoSerializer(ModelSerializer):
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "photos"
        )


