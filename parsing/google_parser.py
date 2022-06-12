import logging
from parse_tass import *
from parse_rbc import *
from lenta import *
from mos import *
from interfax_parse import parse_interfax
from commerce_parse import *
from googlesearch import search
import time
from config import WHITE_LIST
from typing import Dict, List

whitelist_mapping = {
    'interfax.ru': parse_interfax,
    'nauka.tass.ru': parse_tass,
    'www.mos.ru/mayor/themes/': parse_mos,
    'www.mos.ru/news/item/': parse_mos,
    '/www.kommersant.ru/': parse_commerce,
    'https://lenta.ru/news/': parse_lenta,
    '/www.rbc.ru': parse_rbc
}


def get_articles_google(query, whitelist, n)-> List[Dict[str, str]]:
    result_set = []
    for source in whitelist:
        for_search = f'inurl:{source} {query}'
        articles = search(for_search, stop=n)
        for art in articles:
            d = {'name': source}
            d['url'] = art
            news = whitelist_mapping[source](art)
            if news and news['title'] and news['content']:
                d['success'] = True
                d['response'] = news
            else:
                d['success'] = False
                logging.warning(art)
            time.sleep(2)
        result_set.append(d)
    return result_set



if __name__ == '__main__':
    from pprint import pprint

    test_queries = [
        'Москва вошла в топ-3 COVID',
        'Выиграл хакатон',
    ]
    for q in test_queries:
        pprint(get_articles_google(q, WHITE_LIST, 3))
        time.sleep(1)
