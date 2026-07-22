import requests
import os
from bs4 import BeautifulSoup
from test2 import logger


@logger('habr_parser.log')
def get_habr_articles(keywords, url):
    keywords_lower = [kw.lower() for kw in keywords]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    found_articles = []

    for article in articles:
        title_tag = article.find('a', class_='tm-title__link')
        if not title_tag:
            continue

        title_text = title_tag.text.strip()
        title_link = 'https://habr.com' + title_tag.get('href')

        date_tag = article.find('time')
        date = date_tag.get('title') if date_tag else 'Дата не указана'

        text_to_search = article.get_text(separator=' ', strip=True).lower()

        if any(keyword in text_to_search for keyword in keywords_lower):
            found_articles.append((date, title_text, title_link))

    return found_articles


@logger('habr_parser.log')
def print_articles(articles):
    for date, title, link in articles:
        print(f"{date} – {title} – {link}")
    return len(articles)


def main():
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    URL = 'https://habr.com/ru/articles/'

    log_path = 'habr_parser.log'
    if os.path.exists(log_path):
        os.remove(log_path)

    articles = get_habr_articles(KEYWORDS, URL)

    print_articles(articles)

    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()


if __name__ == '__main__':
    main()