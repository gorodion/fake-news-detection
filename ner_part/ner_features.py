import pandas as pd
from translations import TRANSLATIONS
from typing import List, Dict
from translation import TRANSLATIONS


def get_entities_front(extractor, text: str) -> List:
    entities = extractor.get_entities(text)
    if not entities:
        return [text]
    data = []
    for i, (ent, start, end) in enumerate(entities):
        if i == 0 and start != 0:
            data.append(text[:start])
        data.append((text[start:end], ent))
    if end < len(text):
        data.append(text[end:])
    return data


def get_entitiess(extractor, text: str) -> pd.DataFrame:
    data = []
    for ent, start, end in extractor.get_entities(text):
        data.append({'type': TRANSLATIONS[ent] if ent in TRANSLATIONS else ent, 'text': text[start:end]})
    return pd.DataFrame(data)


def compare_texts(extractor, text1: str, text2: str) -> Dict[str, Dict[str, int]]:
    """

    :param text1: original text
    :param text2: copy/match
    :return: dataframe with per-entity intersection and addition metrics
    """
    result = {'addition_number': dict(), 'intersection_number': dict(),
              'addition_words': dict(), 'intersection_words': dict()}
    entities1 = get_entitiess(extractor, text1)
    entities2 = get_entitiess(extractor, text2)
    original1 = entities1['text'].tolist()
    original2 = entities2['text'].tolist()
    words = [word for sentence in original1 for word in sentence.split()] + \
            [word for sentence in original2 for word in sentence.split()]
    print(words)
    print(entities1)
    print(entities2)
    entities1['text'] = entities1['text'].apply(lambda x: stemming(x))
    entities2['text'] = entities2['text'].apply(lambda x: stemming(x))
    stems1 = entities1['text'].tolist()
    stems2 = entities2['text'].tolist()
    stems = [word for sentence in stems1 for word in sentence.split()] + \
            [word for sentence in stems2 for word in sentence.rsplit()]
    print(stems)
    stem2word = {stems[i]:words[i] for i in range(len(stems))}
    for token in set(entities1['type'].tolist() + entities2['type'].tolist() + ['TOTAL']):
        print(token)
        if token != "TOTAL":
            e1 = entities1.loc[entities1['type'] == token]['text'].tolist()
            e2 = entities2.loc[entities2['type'] == token]['text'].tolist()
        else:
            e1 = entities1['text'].tolist()
            e2 = entities2['text'].tolist()
        print(e1, e2)
        e1 = [x.split() for x in e1]
        e2 = [x.split() for x in e2]

        e1 = set([word for sentence in e1 for word in sentence])
        e2 = set([word for sentence in e2 for word in sentence])
        print(e1, e2, len(e1.intersection(e2)), len(e2 - e1))
        # result['intersection_number'][token] = len(e1.intersection(e2))
        # result['addition_number'][token] = len(e2 - e1)

        added_words = e2 - e1
        result['addition_words'][token] = [stem2word[s] for s in added_words]
        result['intersection_words'][token] = [stem2word[s] for s in e1.intersection(e2)]

    return result


if __name__ == "__main__":
    from ner_extractor import Ner_Extractor
    from processing import stemming
    extractor = Ner_Extractor(model_checkpoint="surdan/LaBSE_ner_nerel")
    t1 = "Привет, я - Дмитрий Беляев. Давай поедем второго декабря на хакатон в Перми. Его проводит ВШЭ, приз - два миллиона долларов"
    t2 = "Привет, я - Игорь Боровой. Мы делаем хакатон в Праге, но потом поедем в Пермь."

    print(get_entities_front(extractor, 'Это Москва'))
    print(get_entities_front(extractor, 'Дмитрий есть человек'))
    print(get_entities_front(extractor, 'Дмитрий Беляев'))

    print(get_entitiess(extractor, t1))
    print(get_entitiess(extractor, t2))
    print(compare_texts(extractor, t1, t2))
else:
    from .ner_extractor import Ner_Extractor
    from .processing import stemming