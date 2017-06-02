
from django.db import models

import requests
import urllib.parse
from django.core import files
import tempfile
from rake_nltk import Rake
from news.tasks.techcrunch_helper import TechcrunchHelper
from decimal import Decimal
from django.contrib.humanize.templatetags.humanize import naturaltime


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

    categories = models.ManyToManyField(Category, blank=True)

    # parent = models.ForeignKey("self", blank=True, related_name="children")
    # related_articles = models.ForeignKey("self", blank=True, null=True, related_name="article_related_articles")

    author = models.CharField( max_length=100, null=True )
    description = models.CharField( max_length=500 )
    title = models.CharField( max_length=250, unique=True )
    url = models.CharField(max_length=200)
    url_to_image = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    published = models.DateTimeField(auto_now=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)

    def natural_time(self):
        return naturaltime(self.timestamp)

    def extracted_text(self):
        return ", ".join( kp.text for kp in self.keyphrases.all() )


    def photo_urls(self):
        return [ "/".join(photo.image.name.split("/")[2:]) for photo in self.photos.all() ]

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return str(self.title)

    def save(self, *args, **kwargs):

        # create
        if not self.pk:

            super(Article, self).save(*args, **kwargs)
            print("==> self.title created: ", self.title[:25])

            if self.source == "techcrunch": #do Techcrunch specific logics

                # 1. save related images to the article model, if any
                tch = TechcrunchHelper(self.url)
                image_urls = tch.all_images()
                if image_urls and len(image_urls) >= 1:
                    print("  ==> saving related images: ")
                    # save_image_from_url()
                    for image_url in image_urls:
                        req = requests.get(image_url, stream=True)
                        if req.status_code == 200:
                            filename = urllib.parse.unquote(image_url).split('/')[-1].split('?')[0]
                            # skip blank files from TechCrunch ex: 1x1.jpg
                            if filename.startswith("1x1"):
                                continue

                            tf = tempfile.NamedTemporaryFile()
                            for block in req.iter_content(1024*8):
                                if not block:
                                    break
                                tf.write(block)

                            photo = Photo()
                            photo.image.save(filename, files.File(tf))
                            self.photos.add(photo)
                            print("  ==> <", filename, "> image saved successfully.\n")

                # 2. if text gathered successfully, feed text to Rake, save KP model
                text = tch.all_text()
                if text and len(text) > 100:
                    r = Rake()
                    r.extract_keywords_from_text(text)
                    ph_scores = r.get_ranked_phrases_with_scores()
                    # save score, text to Keyphrase model
                    top_score_tuples = ph_scores[:10]
                    if top_score_tuples and len(top_score_tuples) == 10:
                        for t in top_score_tuples: # (52.8878, 'foo bar baz')
                            kp = Keyphrase()
                            # need try catch
                            kp.score = Decimal(t[0])
                            kp.text = t[1]
                            print("    phrase: " + kp.text + ", score: " + str(round(kp.score, 2)))
                            kp.save()
                            self.keyphrases.add(kp)

                        print("  Keyphrases and scores saved successfully.\n\n")

                    #mentioned_topics
                    print("===> ", tch.mentioned_topics(tch.related_links()))

        # save
        else:
            super(Article, self).save(*args, **kwargs)
            print("==> self.title saved: ", self.title[:15])


class Keyphrase(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="keyphrases", null=True, blank=True)
    text = models.CharField( max_length=100, unique=True )
    score = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal("0.00000"))

    def __str__(self):
        return str(self.text + ": score: " + str(self.score))


class Photo(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="photos", null=True, blank=True)

    image = models.ImageField(upload_to="news/static/news/photos/originals/%Y/%m/")

    # title = models.CharField(max_length=100)
    # image_height = models.IntegerField()
    # image_width = models.IntegerField()
    # caption = models.CharField(max_length=250, blank=True)

