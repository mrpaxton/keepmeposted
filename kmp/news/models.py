
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

    # parent = models.ForeignKey("self", blank=True, related_name="children")
    related_articles = models.ForeignKey("self", null=True, blank=True, related_name="article_related_articles")

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


class Keyphrase(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    text = models.CharField( max_length=100, unique=True )

    def __str__(self):
        return str(self.text)


class Photo(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)

    image = models.ImageField(upload_to="photos/originals/%Y/%m/")

    # title = models.CharField(max_length=100)
    # image_height = models.IntegerField()
    # image_width = models.IntegerField()
    # caption = models.CharField(max_length=250, blank=True)

