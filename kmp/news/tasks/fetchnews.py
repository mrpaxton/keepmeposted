

from django_cron import CronJobBase, Schedule
from django.conf import settings
from datetime import datetime
import requests
import simplejson
from news.models import Article, Category

class FetchNewsJob(CronJobBase):

    RUN_EVERY_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "news.tasks.fetchnews.FetchNewsJob"

    def do(self):
        datafile = settings.BASE_DIR + "/news/tasks/datafile.txt"

        articles = article_models()

        with open(datafile, 'a') as df:
            df.write("Fetched at " + \
                    datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            if articles and len(articles) >= 1:
                for m in articles:
                    df.write("Model saved: " + str(m) + "\n")


# article models by source and cateogry
def article_models():
    sources = [ ("espn", "Sports"), ("bloomberg", "Finance"), ("techcrunch", "Technology") ]
    articles = []
    for source in sources:
        for article in fetch_articles(source[0]):
            article_model = article_to_model(article, source[0], source[1])
            articles.append(article_model)
    return articles

# returns deserialized data
def fetch_articles(source):
    source_url = "https://newsapi.org/v1/articles?source=" + \
            source + "&apiKey=d5a12ea16437480f95bc839a73fb9f04"
    print("Fetching from => " + source_url + " ...")
    response = requests.get(source_url)
    articles = simplejson.loads(response.text).get("articles")
    return articles


# create a model given deserialized data
def article_to_model(article, source, category):
    a = None
    try:
        a = Article.objects.create(
            title=article.get("title"),
            author=article.get("author"),
            description=article.get("description"),
            url=article.get("url"),
            url_to_image=article.get("urlToImage"),
            source=source,
        )
        cat_name = category.upper()
        a.categories.add( Category.objects.get(name=cat_name) )
        a.save()
    except Exception as e:
        print("\t Error creating a model: " + str(e))
    return a

