import requests
import bs4
from typing import Dict, Optional
import logging

def parse_rbc(url: str) -> Optional[Dict[str, str]]:
    try:
        page = requests.get(url)
        if page.status_code != 200:
            return None
        page = page.text
        soup = bs4.BeautifulSoup(page, "html.parser")
        title = soup.find('h1', {'itemprop':'headline'}).contents[0]
        try:
            date = soup.find('span', {'itemprop':'datePublished'}).get('content')
            date = date.rsplit('T')[0]
        except Exception:
            date = soup.find('time', {'class': 'article__header__date'}).get('datetime')[:10]
        content = ' '.join([p.text.replace(u'\xa0', ' ') for p in soup.find('div', {'class':'article__text'}).findAll('p')])
        category = soup.find('a', {'class':'article__header__category'}).contents[0]

        return dict(title=title, category=category, date=date, content=content,)
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    from pprint import pprint
    import time

    test_urls = ['https://www.rbc.ru/technology_and_media/22/12/2015/567966569a7947f4de862d11',
                 'https://www.rbc.ru/technology_and_media/06/02/2018/5a7882029a794765ba37c643']
    for url in test_urls:
        result = parse_rbc(url)
        if result:
            pprint(result)
        else:
            logging.warning(url)
        time.sleep(1)
