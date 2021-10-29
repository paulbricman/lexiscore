from newspaper import Article
import feedparser
from datetime import datetime
from dateutil import parser
from bs4 import BeautifulSoup
import opml
import re
import time
from urllib.parse import urlparse


def fetch_from_opml(filename, max_days_ago):
    aggregate_entries = []

    for feed_entry in opml.parse(filename)[0]:
        feed = feedparser.parse(feed_entry.xmlUrl)
        entries = [e for e in feed['entries'] if (datetime.now() - parser.parse(e['published']).replace(tzinfo=None)).days < max_days_ago]
        
        for e_idx, e in enumerate(entries):
            entries[e_idx]['author'] = feed['feed']['title'] 
        
        aggregate_entries += entries

    aggregate_entries = sorted(aggregate_entries, key=lambda x: parser.parse(x['published']))
    aggregate_contents = [''] * len(aggregate_entries)
    aggregate_titles = [''] * len(aggregate_entries)

    for e_idx, e in enumerate(aggregate_entries):
        if e.get('content') is not None:
            aggregate_contents[e_idx] = e.get('content')[0]['value']
        elif e.get('summary') is not None:
            aggregate_contents[e_idx] = e.get('summary')
        aggregate_titles[e_idx] = e.get('author') + ' | ' + e.get('title')

    aggregate_contents = [BeautifulSoup(e, 'html.parser').get_text() for e in aggregate_contents]
    
    return aggregate_titles, aggregate_contents


def fetch_from_bookmarks(filename, bookmark_folder, max_days_ago):
    raw_bookmark_file = open(filename).read()
    bookmark_soup = BeautifulSoup(raw_bookmark_file, 'html.parser')
    folder_element = [e for e in bookmark_soup.find_all('h3') if re.compile(bookmark_folder).match(e.text)]
    bookmarks = folder_element[0].parent()[1].find_all('a')
    bookmarks = [e for e in bookmarks if (time.time() - float(e['add_date']) < max_days_ago * 60 * 60 * 24)]

    bookmark_contents = []
    bookmark_titles = []

    for bookmark in bookmarks:
        domain = urlparse(bookmark['href']).netloc.replace('www.', '')
        article = Article(bookmark['href'])
        article.build()
        bookmark_contents += [article.text]
        bookmark_titles += [domain + ' | ' + article.title]

    return bookmark_titles, bookmark_contents

'''
import connectors
x=connectors.fetch_from_bookmarks('data/bookmarks.html', 'Blogs', 200)
'''