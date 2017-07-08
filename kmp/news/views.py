
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count

from .models import Article, Category

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import ListAPIView, RetrieveAPIView

from news.serializers import ArticleSerializer, KeyphraseSerializer, ArticlePhotoSerializer, ArticleListSerializer


MAX_NEWS = 20


class ArticleKeyphrasesAPIView(ListAPIView):
    queryset = Article.objects.prefetch_related("keyphrases")
    serializer_class = ArticleSerializer
    lookup_field = "pk"

class ArticlePhotoAPIView(ListAPIView):
    queryset = Article.objects.prefetch_related("photos")
    serializer_class = ArticlePhotoSerializer
    lookup_field = "pk"

class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.prefetch_related("keyphrases")
    serializer_class = ArticleSerializer
    lookup_field = "pk"


class TextScoreAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        articles = Article.objects.prefetch_related("keyphrases")
        test_article = articles.filter(id=3372).first()
        extracted_texts = [ kp.text for kp in test_article.keyphrases.all() ]
        scores = [ kp.score for kp in test_article.keyphrases.all() ]
        data = {
            "labels": extracted_texts,
            "default": scores,
        }
        return Response(data)


class SportsArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
            .filter(categories__name__in=[Category.SPORTS]) \
            .order_by('-timestamp')[:MAX_NEWS]

    def get_context_data(self, **kwargs):
        context = super(SportsArticleListView, self).get_context_data(**kwargs)
        context['headline'] = "Sport News Today"
        return context


class FinanceArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
                .filter(categories__name__in=[Category.FINANCE]) \
                .order_by('-timestamp')[:MAX_NEWS]

    def get_context_data(self, **kwargs):
        context = super(FinanceArticleListView, self).get_context_data(**kwargs)
        context['headline'] = "Financial News"
        return context


class GeneralArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
                .filter(categories__name__in=[Category.GENERAL]) \
                .order_by('-timestamp')[:MAX_NEWS]

    def get_context_data(self, **kwargs):
        context = super(GeneralArticleListView, self).get_context_data(**kwargs)
        context['headline'] = "News Today"
        return context



class TechArticleListView(ListView):

    model = Article

    def get_queryset(self):
        # Expose num_keyphrases: use an annotate function; passing an aggregate function Count
        return Article.objects.annotate(num_keyphrases=Count("keyphrases")) \
                .filter(categories__name__in=[Category.TECH]) \
                .order_by('-timestamp')[:MAX_NEWS]

    def get_context_data(self, **kwargs):
        context = super(TechArticleListView, self).get_context_data(**kwargs)
        context['headline'] = "Tech News for You"
        return context

