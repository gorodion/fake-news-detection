import requests
import bs4
from typing import Dict, Optional
from datetime import datetime


def parse_tass(url: str) -> Optional[Dict[str, str]]:
    try:
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
    except Exception:
        return None

