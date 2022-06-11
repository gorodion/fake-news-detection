import requests
from bs4 import BeautifulSoup


_date_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
_date_num = {date: str(num).zfill(2) for date, num in zip(_date_names, range(1, len(_date_names)+1))}


def _process_lenta_date(date):
    d, m, y = date.split()
    d = d.zfill(2)
    m = _date_num[m]
    return f'{y}-{m}-{d}'


def parse_lenta(url: str) -> dict:
    try:
        req = requests.get(url)
        if req.status_code != 200:
            return None
        soup = BeautifulSoup(req.text, features="lxml")
        date = soup.find('time', attrs={'class': 'topic-header__item topic-header__time'}).text.split(maxsplit=1)[-1]
        date = _process_lenta_date(date)
        # preview = soup.find('div', attrs={'class': 'topic-body__title-yandex'}).text.replace('\xa0', ' ')
        title = soup.find('span', attrs={'class': 'topic-body__title'}).text.replace('\xa0', ' ')
        content = '\n'.join([i.text for i in soup.find_all('p', attrs={'class': 'topic-body__content-text'})]).replace('\xa0', ' ')
        category = soup.find('a', attrs={'class': 'topic-header__item topic-header__rubric'}).text.replace('\xa0', ' ')
        return dict(title=title, content=content, category=category, date=date)
    except Exception as exc:
        return None


if __name__ == '__main__':
    from pprint import pprint
    import time

    test_urls = [
        'https://lenta.ru/news/2022/01/09/zabolevaemost/',
        'https://lenta.ru/news/2022/02/09/consulate/',
        'https://lenta.ru/news/2022/03/09/biolnuland/',
        'https://lenta.ru/news/2022/04/08/morales/',
        'https://lenta.ru/news/2022/05/10/ll/',
        'https://lenta.ru/news/2022/06/10/prices/',
        'https://lenta.ru/news/2021/07/10/slezhka/',
        'https://lenta.ru/news/2021/08/09/uslovie/',
        'https://lenta.ru/news/2021/09/08/zone/',
        'https://lenta.ru/news/2021/10/08/talkov/',
        'https://lenta.ru/news/2021/11/09/aviasoobschenie/',
        'https://lenta.ru/news/2021/12/09/tomas/'
    ]
    for url in test_urls:
        pprint(parse_lenta(url))
        time.sleep(1)
