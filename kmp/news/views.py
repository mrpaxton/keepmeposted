from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView

from .models import Article, Category

from rest_framework.views import APIView
from rest_framework.response import Response


MAX_NEWS = 10


class MockDataAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
         qs_count = 20 #User.objects.all().count()
         labels = ["Users long label name really long label name werwer werw sdfsdf werwer", "Blue foo bar baz yo ho la", "Yellow hello there rad cool dope epic", "Green", "Purple", "Orange", "Teal", "Cyan"]
         default_items = [qs_count, 23, 2, 3, 12, 2, 5, 35]
         data = {
                 "labels": labels,
                 "default": default_items,
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

