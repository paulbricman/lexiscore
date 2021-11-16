from newspaper import Article
import feedparser
from datetime import datetime
import dateutil
from bs4 import BeautifulSoup
import opml
import re
import time
from urllib.parse import urlparse
from ebooklib import epub
from tika import parser
import os
import regex as re


def fetch_from_opml(filename, max_days_ago):
    aggregate_entries = []

    for feed_entry in opml.parse(filename)[0]:
        feed = feedparser.parse(feed_entry.xmlUrl)
        entries = [e for e in feed['entries'] if 'published' in e.keys() and (datetime.now() - dateutil.parser.parse(e['published']).replace(tzinfo=None)).days < max_days_ago]

        for e_idx, e in enumerate(entries):
            entries[e_idx]['author'] = feed['feed']['title'] 
        
        aggregate_entries += entries

    aggregate_entries = sorted(aggregate_entries, key=lambda x: dateutil.parser.parse(x['published']), reverse=True)
    aggregate_contents = [''] * len(aggregate_entries)
    aggregate_titles = [''] * len(aggregate_entries)

    for e_idx, e in enumerate(aggregate_entries):
        if e.get('content') is not None:
            aggregate_contents[e_idx] = e.get('content')[0]['value']
        elif e.get('summary') is not None:
            aggregate_contents[e_idx] = e.get('summary')
        aggregate_titles[e_idx] = e.get('author') + ' | ' + e.get('title')

    raw_contents = aggregate_contents.copy()
    aggregate_contents = [BeautifulSoup(e, 'html.parser').get_text() for e in aggregate_contents]

    data = {}
    for idx in range(len(aggregate_contents)):
        data[aggregate_titles[idx]] = [aggregate_contents[idx], raw_contents[idx]]
    
    return data


def fetch_from_bookmarks(filename, bookmark_folder, max_days_ago):
    raw_bookmark_file = open(filename).read()
    bookmark_soup = BeautifulSoup(raw_bookmark_file, 'html.parser')
    folder_element = [e for e in bookmark_soup.find_all('h3') if re.compile(bookmark_folder).match(e.text)]
    bookmarks = folder_element[0].parent()[1].find_all('a')
    bookmarks = [e for e in bookmarks if (time.time() - float(e['add_date']) < max_days_ago * 60 * 60 * 24)]

    bookmark_contents = []
    bookmark_raw = []
    bookmark_titles = []

    for bookmark in bookmarks:
        domain = urlparse(bookmark['href']).netloc.replace('www.', '')
        article = Article(bookmark['href'])
        article.build()
        bookmark_contents += [article.text]

        raw = article.html
        raw = re.sub(r'<head\s?>[\s\S]*<\/head\s?>', '', raw)

        f = open('./tmp/test.html', 'w+')
        f.write(raw)
        f.close()
        #print('NEW BOOKMARK RAW', raw)

        bookmark_raw += [raw]
        bookmark_titles += [domain + ' | ' + article.title]

    data = {}
    for idx in range(len(bookmark_contents)):
        data[bookmark_titles[idx]] = [bookmark_contents[idx], bookmark_raw[idx]]
    
    return data


def fetch_from_epub(filename):
    book = epub.read_epub(filename)
    content = sorted([e.content for e in book.items if isinstance(e, epub.EpubHtml)], key=lambda x: len(x), reverse=True)[0]
    processed = BeautifulSoup(content, 'html.parser').get_text()
    
    data = {}
    data[book.get_metadata('DC', 'creator')[0][0] + ' | ' + book.title] = [processed, content.decode('utf-8')]
    
    return data


def fetch_from_pdf(filename):
    doc = parser.from_file(filename)

    data = {}
    data[doc['metadata']['Author'] + ' | ' + doc['metadata']['pdf:docinfo:title']] = [doc['content'], doc['content']]

    return data


def fetch_from_plaintext(filename):
    text = open(filename).read()
    raw = '\n'.join(['<p>' + e + '</p>' for e in text.split('\n')])

    data = {}
    data[os.path.splitext(os.path.basename(filename))[0]] = [text, raw]

    return data


