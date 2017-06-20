from django.contrib import admin

# Register your models here.

from .models import Article, Category, Keyphrase, RelatedTopic

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Keyphrase)
admin.site.register(RelatedTopic)
