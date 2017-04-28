

from django.conf.urls import url
from django.contrib import admin

from .views import (
    FinanceArticleListView,
    GeneralArticleListView,
    SportsArticleListView,
    TechArticleListView,
)


urlpatterns = [
    url( r'^$|general$', GeneralArticleListView.as_view(), name="general-article-list"),
    url( r'^finance', FinanceArticleListView.as_view(), name="finance-article-list"),
    url( r'^sports', SportsArticleListView.as_view(), name="sports-article-list"),
    url( r'^tech', TechArticleListView.as_view(), name="tech-article-list"),
]

