
from django.db import models

import requests
import urllib.parse
from django.core import files
import tempfile
import re
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
        keyphrases = [self.__text_without_puncs(kp.text) for kp in self.keyphrases.all()]
        return ", ".join(kp for kp in keyphrases)

    def photo_urls(self):
        return [ "/".join(photo.image.name.split("/")[2:]) for photo in self.photos.all() ]

    def save(self, *args, **kwargs):
        # create an article object
        if not self.pk:
            super(Article, self).save(*args, **kwargs)

            print("==> Article created. Title: ", self.title[:25] + "...")

            if self.source == "techcrunch": #do Techcrunch specific logics

                # 1. save related images to the article model, if any
                tch = TechcrunchHelper(self.url)
                all_images = tch.all_images()
                self.__save_images(all_images)

                # 2. if text gathered successfully, feed text to Rake, save keyphrases in KP model
                text = tch.all_text()
                self.__save_keyphrases(text)

                # 3. save related topics retrieved from the related URL slugs by TC
                #mentioned_topics
                related_links = tch.related_links()
                mentioned_topics = tch.mentioned_topics(related_links)
                self.__save_related_topics(mentioned_topics)

        else: # save an article object
            super(Article, self).save(*args, **kwargs)
            print("==> Article saved. Title: ", self.title[:30] + "...")


    def __text_without_puncs(self, text):
        return re.sub("[^a-zA-Z0-9 \n]", "", text)


    def __save_related_topics(self, topics):
        if topics and len(topics) > 1:
            for topic in topics:
                rt = RelatedTopic()
                rt.link = topic
                rt.save()
                self.related_topics.add(rt)
                print("  ==> Related topic: ", topic, " saved successfully.")


    def __save_images(self, image_urls):
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


    def __save_keyphrases(self, text):
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

    def __str__(self):
        return str(self.title)

    def __unicode__(self):
        return str(self.title)


class RelatedTopic(models.Model):

    article = models.ForeignKey(
            Article,
            on_delete=models.CASCADE,
            related_name="related_topics",
            null=True,
            blank=True
    )
    link = models.CharField(max_length=200)

    def __str__(self):
        return str("Related topic: " + self.link)


class Keyphrase(models.Model):

    article = models.ForeignKey(
            Article,
            on_delete=models.CASCADE,
            related_name="keyphrases",
            null=True,
            blank=True
    )
    text = models.CharField( max_length=100, unique=True )
    score = models.DecimalField(max_digits=10, decimal_places=5,
        default=Decimal("0.00000"))

    def __str__(self):
        return str(self.text + ": score: " + str(self.score))



class Photo(models.Model):

    article = models.ForeignKey(
            Article,
            on_delete=models.CASCADE,
            related_name="photos",
            null=True,
            blank=True
    )
    image = models.ImageField(upload_to="news/static/news/photos/originals/%Y/%m/")

    def __str__(self):
        return str(self.image)

