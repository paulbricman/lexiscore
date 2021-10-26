from newspaper import Article


def fetch_from_online_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text, 'online article'