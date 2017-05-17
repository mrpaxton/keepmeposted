
from django_cron import CronJobBase, Schedule
from django.conf import settings
from datetime import datetime
import requests
import simplejson
from news.models import Article, Category, Photo


import urllib.parse
import tempfile
from django.core import files
from bs4 import BeautifulSoup

from rake_nltk import Rake



class FetchNewsJob(CronJobBase):

    RUN_EVERY_MINS = 120

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "news.tasks.fetchnews.FetchNewsJob"

    def do(self):

        articles = article_models()

        #log the fetch results: should be moving to when saving model
        datafile = settings.BASE_DIR + "/news/tasks/datafile.txt"
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
        # upon creating an article model:

        #TODO: save related images to the database, using Article.photo.image
        if source == "techcrunch":
            # if related_images: save_images_to_article_model()
            image_urls = techcrunch_images(article.get("url"))
            if image_urls and len(image_urls) >= 1:
                print("Saving related images => ", image_urls)
                for image_url in image_urls:
                    req = requests.get(image_url, stream=True)
                    if req.status_code == 200:
                        filename = urllib.parse.unquote(image_url).split('/')[-1].split('?')[0]
                        tf = tempfile.NamedTemporaryFile()
                        for block in req.iter_content(1024*8):
                            if not block:
                                break
                            tf.write(block)
                        photo = Photo()
                        photo.image.save(filename, files.File(tf))
                        a.photos.add(photo)
                        print(filename, " saved successfully.\n")


            # TODO: extract key phrases using RAKE algo and save to database
            # 1. gather article text
            # 2. if text gathered successfully, feed text to Rake
            # 3. result from Rake is saved to database, need a model
                # Key Phrase: belongs to Article, text, score
            r = Rake()
            text = techcrunch_all_text(article.get("url"))
            r.extract_keywords_from_text(text)
            ph_scores = r.get_ranked_phrases_with_scores()
            print(ph_scores)
            print("===================")

        # Save category
        cat_name = category.upper()
        a.categories.add( Category.objects.get(name=cat_name) )

        a.save()

    except Exception as e:
        print("\t Error creating a model: " + str(e))
    return a

# helper to get all text from Techcrunch url
def techcrunch_all_text(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    all_p = soup.select("article p")
    news_text = [ p.text for p in all_p ]
    return " ".join(news_text)

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
