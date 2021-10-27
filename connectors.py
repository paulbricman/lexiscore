from newspaper import Article
import feedparser
from datetime import datetime
from dateutil import parser
from bs4 import BeautifulSoup


def fetch_from_online_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, [article.text], 'online article'


def fetch_from_rss_feed(url, days):
    feed = feedparser.parse(url)
    entries = [e for e in feed['entries'] if (datetime.now() - parser.parse(e['published']).replace(tzinfo=None)).days < days]
    contents = [e['content'][0]['value'] for e in entries]
    contents = [BeautifulSoup(e, 'html.parser').get_text() for e in contents]
    return feed['feed']['title'], contents, 'RSS feed'
