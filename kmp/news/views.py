from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView

from .models import Article, Category

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import ListAPIView, RetrieveAPIView

from news.serializers import ArticleSerializer, KeyphraseSerializer

MAX_NEWS = 10


class ArticleKeyphrasesAPIView(ListAPIView):
    queryset = Article.objects.prefetch_related("keyphrases")
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.prefetch_related("keyphrases")
    serializer_class = ArticleSerializer
    lookup_field = "pk"


class TextScoreAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        articles = Article.objects.prefetch_related("keyphrases")
        test_article = articles.filter(id=1910).first()
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
        return Article.objects \
                .filter(categories__name__in=[Category.TECH]) \
                .order_by('-timestamp')[:MAX_NEWS]

    def get_context_data(self, **kwargs):
        context = super(TechArticleListView, self).get_context_data(**kwargs)
        context['headline'] = "Tech News for You"
        return context

