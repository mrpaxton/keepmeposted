

from bs4 import BeautifulSoup
import requests


class TechcrunchHelper:


    def __init__(self, url):
        self.url = url
        html_doc = requests.get(url).text
        self.soup = BeautifulSoup(html_doc, "html.parser")


    def all_text(self):

        """
            A helper function to get all text from Techcrunch url
            @return A combined string of news text
        """

        all_p = self.soup.select("article p")
        news_text = [ p.text for p in all_p ]
        return " ".join(news_text)


    def all_images(self):

        """
            A helper function to extract images from TechCrunch news
            @return A list of all images
        """

        big_images = [ i.get("src") for i in self.soup.select("div.article-entry img") ]
        slide_images = [ i.get("data-src") for i in self.soup.select("div.slideshowify li div.image img") ]
        return big_images + slide_images


    # private helper to convert link into unslugified text
    def unslugify(self, url):
        if not url:
            return None
        url = url.rstrip("/")
        return url.split("/")[-1].replace("-", " ").capitalize()


    # helper to extract related links from TechCrunch news
    # returns a dictionary of links that has l.text, l["href"], etc
    def related_links(self):
        links = self.soup.select("div.article-entry p a")
        return [ (l.text, l["href"], self.unslugify(l.get("href"))) for l in links ]


    # private helper, input argument is the output from related_links() method
    def mentioned_topics(self, t_links):
        topics = [ max( [ t[0], t[2] ], key=lambda x: len(x) ) for t in t_links ]
        sorted_topics = sorted(topics, key=lambda x: -len(x))
        return sorted_topics[:10]
