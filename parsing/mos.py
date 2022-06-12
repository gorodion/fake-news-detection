import requests
from bs4 import BeautifulSoup


def parse_mos(url: str) -> dict:
    try:
        req = requests.get(url)
        if req.status_code != 200:
            return None
        soup = BeautifulSoup(req.text, features="lxml")
        date = soup.find('time', attrs={'class': 'news-article__date'}).get('datetime').split()[0]
        title = soup.find('h1', attrs={'class': 'news-article-title-container__title'}).text.replace('\xa0', ' ')
        # preview = soup.find('div', attrs={'class': 'news-article__preview'}).text.replace('\xa0', ' ')
        content = soup.find('div', attrs={'class': 'content-text'}).text.replace('\xa0', ' ')
        category = soup.find('a', attrs={'class': 'news-article-spheres__link'}).text.replace('\xa0', ' ')
        return dict(title=title, content=content, category=category, date=date)
    except Exception as e:
        print(f'Failed to parse mos.ru {e}')
        return None


if __name__ == '__main__':
    from pprint import pprint
    import time

    test_urls = [
        'https://www.mos.ru/mayor/themes/12299/8381050/',
        'https://www.mos.ru/mayor/themes/4299/8380050/',
        'https://www.mos.ru/news/item/108039073/'
        'https://www.mos.ru/news/item/108162073/',
    ]
    for url in test_urls:
        pprint(parse_mos(url))
        time.sleep(1)
