
from django_cron import CronJobBase, Schedule
from django.conf import settings
from datetime import datetime
import requests
import simplejson
from news.models import Article, Category, Photo


class FetchNewsJob(CronJobBase):

    RUN_EVERY_MINS = 120

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "news.tasks.fetchnews.FetchNewsJob"

    def do(self):
        articles = article_models()


# article models by source and cateogry
def article_models():
    sources = [
        ("espn", "Sports"),
        ("bloomberg", "Finance"),
        ("techcrunch", "Technology")
    ]
    for source in sources:
        for article in fetch_articles(source[0]):
            article_model = article_to_model(article, source[0], source[1])
            if article_model:
                #log the fetch results: should be moving to when saving model
                datafile = settings.BASE_DIR + "/news/tasks/datafile.txt"
                with open(datafile, 'a') as df:
                    df.write("Fetched at " + \
                            datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                    output = ": ".join(["Model saved", article_model.source, article_model.title])
                    # ignore characters that cannot be printed
                    df.write(output.encode("ascii", "ignore").decode("utf-8"))
                    df.write("\n----------------------- \n")


# fetch articles from source
# returns deserialized data, not yet models
def fetch_articles(source):
    source_url = "https://newsapi.org/v1/articles?source=" + \
            source + "&apiKey=d5a12ea16437480f95bc839a73fb9f04"
    print("Fetching from => " + source + " ..")
    response = requests.get(source_url)
    articles = simplejson.loads(response.text).get("articles")
    # filter only articles whose titles not in database
    existing_titles = [ a.title for a in Article.objects.all() ]
    articles = [ a for a in articles if a["title"] not in existing_titles ]
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
        category = Category.objects.get(name=category.upper())
        a.categories.add(category)

    except Exception as e:
        print("\t Error creating a model: " + str(e))
    return a

