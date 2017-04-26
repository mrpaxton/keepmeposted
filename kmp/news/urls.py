

from django.conf.urls import url
from django.contrib import admin

from .views import (
    ArticleListView,
)

urlpatterns = [
    url( r'^$', ArticleListView.as_view(), name="article-list"),
]

