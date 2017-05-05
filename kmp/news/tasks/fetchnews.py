
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
                    output = ": ".join(["Model saved", m.source, m.title])
                    # ignore characters that cannot be printed
                    df.write(output.encode("ascii", "ignore").decode("utf-8"))
            df.write("\n----------------------- \n")


# article models by source and cateogry
def article_models():
    sources = [
        ("espn", "Sports"),
        ("bloomberg", "Finance"),
        ("techcrunch", "Technology")
    ]
    articles = []
    for source in sources:
        for article in fetch_articles(source[0]):
            article_model = article_to_model(article, source[0], source[1])
            if article_model:
                articles.append(article_model)
    return articles


# returns deserialized data
def fetch_articles(source):
    source_url = "https://newsapi.org/v1/articles?source=" + \
            source + "&apiKey=d5a12ea16437480f95bc839a73fb9f04"
    print("Fetching from => " + source + " ..")
    response = requests.get(source_url)
    articles = simplejson.loads(response.text).get("articles")
    #filter only articles whose titles not in database
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
        cat_name = category.upper()
        a.categories.add( Category.objects.get(name=cat_name) )
        a.save()
    except Exception as e:
        print("\t Error creating a model: " + str(e))
    return a


# helper to extract images from TechCrunch news
def techcrunch_images(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    big_images = [ i.get("src") for i in soup.select("div.article-entry img") ]
    slide_images = [ i.get("data-src") for i in soup.select("div.slideshowify li div.image img") ]
    return big_images + slide_images


# helper to convert link into unslugified text
def unslugify(url):
    if not url:
        return None
    url = url.rstrip("/")
    return url.split("/")[-1].replace("-", " ").capitalize()


# helper to extract related links from TechCrunch news
# returns a dictionary of links that has l.text, l["href"], etc
def techcrunch_related_links(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    links = soup.select("div.article-entry p a")
    return [ (l.text, l["href"], unslugify(l.get("href")) ) for l in links ]


# input argument is the output type of techcrunch_related_links() method
def mentioned_topics(t_links):
    topics = [ max( [ t[0], t[2] ], key=lambda x: len(x) ) for t in t_links ]
    sorted_topics = sorted(topics, key=lambda x: -len(x))
    return sorted_topics[:5]
