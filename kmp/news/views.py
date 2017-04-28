from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView

from .models import Article, Category



class SportsArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
            .filter(categories__name__in=[Category.SPORTS]) \
            .order_by('title')[:5]



class FinanceArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
                .filter(categories__name__in=[Category.FINANCE]) \
                .order_by('title')[:5]



class GeneralArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
                .filter(categories__name__in=[Category.GENERAL]) \
                .order_by('title')[:5]



class TechArticleListView(ListView):

    model = Article

    def get_queryset(self):
        return Article.objects \
                .filter(categories__name__in=[Category.TECH]) \
                .order_by('title')[:5]


