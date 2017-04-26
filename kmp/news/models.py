from django.db import models

# Create your models here.

class Article(models.Model):

    author = models.CharField( max_length=100, null=True )
    description = models.CharField( max_length=500 )
    title = models.CharField( max_length=250 )
    url = models.CharField(max_length=200)
    url_to_image = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return str(self.title)
