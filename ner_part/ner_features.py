import pandas
import pandas as pd
from ner_extractor import Ner_Extractor
from processing import stemming
from typing import Dict

extractor = Ner_Extractor(model_checkpoint = "surdan/LaBSE_ner_nerel")


def get_entitiess(text: str)->pd.DataFrame:
    data = []
    for ent, start, end in extractor.get_entities(text):
        data.append({'type':ent, 'text': text[start:end]})
    return pd.DataFrame(data)


def compare_texts(text1: str, text2: str)->Dict[str, Dict[str, int]]:
    """

    :param text1: original text
    :param text2: copy/match
    :return: dataframe with per-entity intersection and addition metrics
    """
    result = {'addition': dict(), 'intersection':dict()}
    entities1 = get_entitiess(text1)
    entities2 = get_entitiess(text2)
    print(entities1)
    print(entities2)
    entities1['text'] = entities1['text'].apply(lambda x: stemming(x))
    entities2['text'] = entities2['text'].apply(lambda x: stemming(x))
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
        result['intersection'][token] = len(e1.intersection(e2))
        result['addition'][token] = len(e2 - e1)
    return result


if __name__ == "__main__":
    t1 = "Привет, я - Дмитрий Беляев. Давай поедем второго декабря на хакатон в Перми. Его проводит ВШЭ, приз - два миллиона долларов"
    t2 = "Привет, я - Игорь Боровой. Мы делаем хакатон в Праге, но потом поедем в Пермь."
    print(get_entitiess(t1))

    print(get_entitiess(t2))

    print(compare_texts(t1, t2))