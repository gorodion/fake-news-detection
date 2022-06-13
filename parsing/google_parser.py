import logging
from googlesearch import search
import time
from typing import Dict, List


from .parse_tass import *
from .parse_rbc import *
from .lenta import *
from .mos import *
from .interfax_parse import parse_interfax
from .commerce_parse import *
from cfg import *

source_dict = {
    'interfax.ru': ['interfax.ru'],
    'nauka.tass.ru': ['nauka.tass.ru'],
    'mos.ru': ['www.mos.ru/mayor/themes/', 'www.mos.ru/news/item/'],
    'kommersant.ru': ['www.kommersant.ru/'],
    'lenta.ru': ['https://lenta.ru/news/'],
    'rbc.ru': ['www.rbc.ru']
}

whitelist_mapping = {
    'interfax.ru': parse_interfax,
    'nauka.tass.ru': parse_tass,
    'www.mos.ru/mayor/themes/': parse_mos,
    'www.mos.ru/news/item/': parse_mos,
    'www.kommersant.ru/': parse_commerce,
    'https://lenta.ru/news/': parse_lenta,
    'www.rbc.ru': parse_rbc
}


def get_articles_google(query, whitelist, n=1) -> List[Dict[str, str]]:
    sources = []
    print(whitelist)
    for source in whitelist:
        for source_url in source_dict[source]:
            for_search = f'inurl:{source_url} {query}'
            articles = search(for_search, stop=n)
            d = {NAME: source, SUCCESS: False}
            for art in articles:
                d['url'] = art
                news = whitelist_mapping[source_url](art)
                if news and news['title'] and news['content']:
                    d[SUCCESS] = True
                    d[RESPONSE] = news
                # else:
                #     d[SUCCESS] = False
                #     logging.warning(art)
            time.sleep(2)
            sources.append(d)
    return sources



if __name__ == '__main__':
    from pprint import pprint

    test_queries = [
        'Москва стала лидером в Европе в рейтинге инноваций, помогающих в борьбе с COVID-19'
    ]
    for q in test_queries:
        pprint(get_articles_google(q, ['mos.ru', 'rbc.ru'], 3))
        time.sleep(1)
