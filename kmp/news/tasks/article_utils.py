

from django.conf import settings
from datetime import datetime
import requests
import simplejson
from news.models import Article, Category, Photo


NEWSAPI_URL = "https://newsapi.org/v1/articles?source="
API_KEY = "&apiKey=d5a12ea16437480f95bc839a73fb9f04"

# Function to create an article model by source and cateogry
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
                # Log the fetch results: should be moving to when saving model
                datafile = settings.BASE_DIR + "/news/tasks/datafile.txt"
                with open(datafile, 'a') as df:
                    df.write("Fetched at " + \
                            datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                    output = ": ".join(["Model saved", article_model.source, article_model.title])
                    # ignore characters that cannot be printed
                    df.write(output.encode("ascii", "ignore").decode("utf-8"))
                    df.write("\n----------------------- \n")


# Function to fetch articles from source
# Returns deserialized data, not yet models
def fetch_articles(source):

    source_url = NEWSAPI_URL + source + API_KEY
    print("Fetching from => " + source + " ..")

    try:
        response = requests.get(source_url)
        articles = simplejson.loads(response.text).get("articles")
        # Filter only articles whose titles not in database
        existing_titles = [ a.title for a in Article.objects.all() ]
        articles = [ a for a in articles if a["title"] not in existing_titles ]
        return articles
    except:
        print("Error fetching articles.")
        raise


# Create a model given deserialized data
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
