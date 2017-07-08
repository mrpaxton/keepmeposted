
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include, url

from news.views import (
    TextScoreAPIView,
    ArticleKeyphrasesAPIView,
    ArticleListAPIView,
    ArticleRetrieveAPIView,
    ArticlePhotoAPIView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', include("news.urls", namespace="news")),

    # expose API endpoints for visualization purposes
    url(r'^api/textscores/data/', TextScoreAPIView.as_view()),
    url(r'^api/keyphrase-list/$', ArticleKeyphrasesAPIView.as_view(), name="api-article-list"),
    url(r'^api/articles/$', ArticleListAPIView.as_view(), name="api-article-list"),
    url(r'^api/articles/(?P<pk>[\d]+)/$', ArticleRetrieveAPIView.as_view(), name="api-article-detail"),
    url(r'^api/photo-list/$', ArticlePhotoAPIView.as_view(), name="api-article-photo-list"),
]






