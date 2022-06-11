import requests
import bs4
from typing import Dict, Optional
from datetime import datetime
import logging

def old_parse_tass(url: str) -> Optional[Dict[str, str]]:
    try:
        page = requests.get(url)
        if page.status_code != 200:
            print(page)
            return None
        page = page.text
        soup = bs4.BeautifulSoup(page, "html.parser")
        title = soup.find('span', {'class':'explainer__title'}).contents[0]
        lead = soup.find('div', {'class':'explainer-lead'}).contents[0]
        time = soup.find('dateformat').get('time')
        time = datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d')
        content = lead + ' '.join([p.text.replace(u'\xa0', ' ') for p in soup.find('div', {'class':'card'}).findAll('p')])
        try:
            category = soup.findAll('a', {'class':'tags__item'})[-1].contents[0]
        except Exception:
            category = None
        return dict(title=title, category=category, time=time, content=content,)
    except Exception as e:
        print(e)
        return None

def new_parse_tass(url: str) -> Optional[Dict[str, str]]:
    page = requests.get(url)
    if page.status_code != 200:
        print(page)
        return None
    page = page.text
    soup = bs4.BeautifulSoup(page, "html.parser")
    title = soup.find('h1', {'class':'news-header__title'}).contents[0].replace('\n', '')
    lead = soup.find('div', {'class':'news-header__lead'}).contents[0]
    time = soup.find('dateformat').get('time')
    time = datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d')
    content = lead + ' '.join([p.text.replace(u'\xa0', ' ') for p in soup.find('div', {'class':'text-block'}).findAll('p')])
    category = soup.findAll('a', {'class':'tags__item'})[-1].contents[0]
    return dict(title=title, category=category, time=time, content=content,)



def parse_tass(url: str) -> Optional[Dict[str, str]]:
    try:
        return new_parse_tass(url)
    except Exception:
        pass
    try:
        return old_parse_tass(url)
    except Exception:
        return None

if __name__ == '__main__':
    from pprint import pprint
    import time

    test_urls = [
        'https://nauka.tass.ru/tech/6820121',
        'https://nauka.tass.ru/lyudi-i-veschi/6822824'
        'https://nauka.tass.ru/nauka/13508591',
        'https://nauka.tass.ru/nauka/9108409',
        'https://nauka.tass.ru/nauka/14841837',
        'https://nauka.tass.ru/nauka/14846525',
        'https://nauka.tass.ru/nauka/9333735',
        'https://nauka.tass.ru/nauka/8503609'
    ]
    for url in test_urls:
        result = parse_tass(url)
        if result:
            pprint(result)
        else:
            logging.warning(url)
        time.sleep(1)
        break