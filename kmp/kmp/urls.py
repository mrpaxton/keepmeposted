
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include, url

from news.views import MockDataAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', include("news.urls", namespace="news")),

    url(r'^api/mock/data/', MockDataAPIView.as_view()),
]
