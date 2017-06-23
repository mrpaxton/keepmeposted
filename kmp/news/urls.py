

from django.conf.urls import url
from django.contrib import admin

from .views import (
    FinanceArticleListView,
    GeneralArticleListView,
    SportsArticleListView,
    TechArticleListView,

    ArticleKeyphrasesAPIView,
    ArticleRetrieveAPIView,

    ArticlePhotoAPIView,
)


urlpatterns = [
    url( r'^$|general$', GeneralArticleListView.as_view(), name="general-article-list"),
    url( r'^finance', FinanceArticleListView.as_view(), name="finance-article-list"),
    url( r'^sports', SportsArticleListView.as_view(), name="sports-article-list"),
    url( r'^tech', TechArticleListView.as_view(), name="tech-article-list"),

    url(r'^list/$', ArticleKeyphrasesAPIView.as_view(), name="api-article-list"),
    url(r'^(?P<pk>[\d]+)/$', ArticleRetrieveAPIView.as_view(), name="api-article-detail"),

    url(r'^article-photo-list/$', ArticlePhotoAPIView.as_view(), name="api-article-photo-list"),

]

