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
        articles = search(for_search, stop=n)
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
        'Купил стартап'
    ]
    for q in test_queries:
        pprint(get_articles_google(q, whitelist, 1))
        time.sleep(1)
