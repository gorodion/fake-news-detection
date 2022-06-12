import requests
from bs4 import BeautifulSoup

def parse_interfax(url):
    try:
        page = requests.get(url)
        #set encoding for interfax
        page.encoding = 'ptcp154' 
        if page.status_code != 200:
            return None
        #init BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")
        #taking header
        try:
            title = soup.find('h1', itemprop="headline").text
        except Exception as e:
            print(f'Failed to parse title {e}')
        #taking content
        try:
            content = ' '.join(list(map(lambda x : x.text, soup.findAll('p'))))
        except Exception as e:
            print(f'Failed to parse content {e}')
        #taking category
        try:
            category = soup.find('aside', class_="textML").contents[1].text
        except Exception as e:
            print(f'Failed to parse category {e}')
        #taking date
        try:
            date = soup.find('a',class_="time")["href"][6:].replace('/', '-')
        except Exception as e:
            print(f'Failed to parse date {e}')
        #return dict with all information
        return dict(title=title, content=content, category=category, date=date)
    except Exception:
        return None