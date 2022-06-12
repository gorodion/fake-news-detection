import requests
from bs4 import BeautifulSoup

def parse_commerce(url):
    try:
        page = requests.get(url)
        #set encoding for interfax
        page.encoding = 'cp65001' 
        if page.status_code != 200:
            return None
        #init BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")        
        #taking header
        title = soup.find('h1', itemprop="headline").text
        #taking content
        content = ' '.join(list(map(lambda x : x.text, soup.findAll('p')))) 
        #taking category
        category = soup.find('li', class_="crumbs__item").contents[1].text
        #taking date
        date = soup.find('time')["datetime"][:10]

        #return dict with all information
        return dict(title=title, content=content, category=category, date=date)
    except Exception:
        return None