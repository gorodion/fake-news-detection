def parse_interfax(url):
    try:
        page = requests.get(url)
        #set encoding for interfax
        page.encoding = 'ptcp154' 
        if page.status_code =! 200:
            return None
        #init BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")
        #taking header
        title = soup.find('h1', itemprop="headline").text
        #taking content
        content = ' '.join(list(map(lambda x : x.text, soup.findAll('p')))) 
        #taking category
        category = soup.find('aside', class_="textML").contents[1].text
        #taking date
        date = soup.find('a',class_="time")["href"][6:].replace('/', '-')

        #return dict with all information
        return dict(title=title, content=content, category=category, date=date)
    except Exception:
        return None