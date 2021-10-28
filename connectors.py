import dateutil
from newspaper import Article
import feedparser
from datetime import date, datetime
from dateutil import parser
from bs4 import BeautifulSoup
import opml


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
    
    return aggregate_titles, aggregate_contents, 'RSS feed'
