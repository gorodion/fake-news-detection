import requests
import bs4
from typing import Dict, Optional


def parse_rbc(url: str) -> Optional[Dict[str, str]]:
    try:
        page = requests.get(url)
        if page.status_code != 200:
            return None
        page = page.text
        soup = bs4.BeautifulSoup(page, "html.parser")
        title = soup.find('h1', {'itemprop':'headline'}).contents[0]
        time = soup.find('span', {'itemprop':'datePublished'}).get('content')
        time = time.rsplit('T')[0]
        content = ' '.join([p.text.replace(u'\xa0', ' ') for p in soup.find('div', {'class':'article__text'}).findAll('p')])
        category = soup.find('a', {'class':'article__header__category'}).contents[0]

        return dict(title=title, category=category, time=time, content=content,)
    except Exception:
        return None

