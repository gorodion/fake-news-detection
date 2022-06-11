import logging
from parse_tass import *
from parse_rbc import *
from lenta import *
from mos import *
from interfax_parse import parse_interfax
from commerce_parse import *
from googlesearch import search
import time

whitelist = {
    'interfax.ru': parse_interfax,
    'nauka.tass.ru': parse_tass,
    'www.mos.ru/mayor/themes/': parse_mos,
    'www.mos.ru/news/item/': parse_mos,
    '/www.kommersant.ru/': parse_commerce,
    'https://lenta.ru/news/': parse_lenta,
    '/www.rbc.ru': parse_rbc
}


def get_articles_google(query, whitelist, n):
    result_set = {source: [] for source in whitelist.keys()}
    for source, func in whitelist.items():
        for_search = f'inurl:{source} {query}'
        time.sleep(1)
        articles = list(search(for_search, stop=n, user_agent="Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"))
        time.sleep(1)
        if len(articles) == 0:
            logging.warning(f'В {source} нет подобных статей')
        time.sleep(1)
        for art in articles:
            news = func(art)
            if news:
                result_set[source].append(news)
            else:
                logging.warning(art)
            time.sleep(1)
    return result_set



if __name__ == '__main__':
    from pprint import pprint

    test_queries = [
        'Илон Маск запустил ракету'
    ]
    for q in test_queries:
        pprint(get_articles_google(q, whitelist, 1))
        time.sleep(1)
