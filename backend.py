from typing import List
from pprint import pprint

from semantic.model import SemanticModel
from ner_part.ner_extractor import Ner_Extractor
from ner_part.ner_features import get_entities_front, compare_texts
from parsing.google_parser import get_articles_google
from summarization.summarizer import get_summary
from cfg import *

semantic_model = SemanticModel(semantic_model_path, semantic_model_name, device)
ner_model = Ner_Extractor(model_checkpoint=ner_model_name)


def has_primary(sources: list) -> bool:
     return bool([source for source in sources
             if source[SUCCESS]
             and source[RESPONSE][DATE]
             and source[RESULT][SEMANTIC] > semantic_thr])


def get_primary_idx(sources: list) -> int:
    return [i for i, source in enumerate(sources)
                 if source[SUCCESS]
                 and source[RESPONSE][DATE] is not None
                 and source[RESULT][SEMANTIC] > semantic_thr][0]


def check_news(title: str, content: str, whitelist: List[str]):
    assert title
    assert content
    assert whitelist

    response = {}

    # с помощью гугла находим похожие источники по заголовку
    sources = get_articles_google(title, whitelist)
    response[SOURCES] = sources
    # кликбейтность
    response[CLICKBAIT] = round((1 - semantic_model(title, content)) * 100)
    # с помощью модели суммаризации получаем суммаризованный контент
    summary = get_summary(content)
    # извлекаем сущности, с помощью NER модели
    ner_content = get_entities_front(ner_model, summary)
    response[NER_CONTENT] = ner_content

    # случай, когда не найдены статьи с похожим заголовком
    found = False
    for source in sources:
        if source[SUCCESS]:
            found = True
            break
    if not found:
        print('Статьи не найдены')
        response[STATUS] = NOT_FOUND
        response[SCORE] = 0

        print('Ответ:')
        pprint(response)
        return response

    # запуск моделей на найденных статьях
    print('Найдены похожие статьи')
    pprint(sources)
    for source in sources:
        if source[SUCCESS]:
            result = {}
            other_summary = get_summary(source[RESPONSE][CONTENT])
            result[NER_CONTENT] = get_entities_front(ner_model, other_summary)
            result[SEMANTIC] = round(semantic_model(other_summary, summary) * 100)
            result[CLICKBAIT] = round((1 - semantic_model(source[RESPONSE][TITLE], other_summary)) * 100)
            ner_compare = compare_texts(ner_model, other_summary, summary)
            result[NER_INTER] = ner_compare['intersection_words']['TOTAL']
            result[NER_ADD] = ner_compare['addition_words']['TOTAL']
            source[RESULT] = result

    # случай, когда нет первоисточника
    if not has_primary(sources):
        print('Нет первоисточника')
        response[STATUS] = NO_PRIMARY
        response[SCORE] = 0 # TODO сделать оценку на основе тональности

        print('Ответ:')
        pprint(response)
        return response

    # ставим первоисточник на первое место
    idx = get_primary_idx(sources)
    sources[0], sources[idx] = sources[idx], sources[0]
    print(f'Первоисточник найден')
    pprint(sources[0])
    # TODO метаоценщик
    response[STATUS] = WITH_PRIMARY
    response[SCORE] = 80 # TODO

    print('Ответ:')
    pprint(response)
    return response
