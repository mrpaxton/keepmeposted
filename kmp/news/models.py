
from django.db import models


class Category(models.Model):

    FINANCE = "FINANCE"
    GENERAL = "GENERAL"
    SPORTS = "SPORTS"
    TECH = "TECHNOLOGY"

    CATEGORY_CHOICES = (
        (FINANCE, "Finance"),
        (GENERAL, "General"),
        (SPORTS, "Sports"),
        (TECH, "Technology"),
    )

    name = models.CharField(
        max_length = 20,
        unique = True,
        choices = CATEGORY_CHOICES,
        default = GENERAL,
    )

    def __str__(self):
        return str(self.name)



class Article(models.Model):

    categories = models.ManyToManyField(Category)

    author = models.CharField( max_length=100, null=True )
    description = models.CharField( max_length=500 )
    title = models.CharField( max_length=250, unique=True )
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
