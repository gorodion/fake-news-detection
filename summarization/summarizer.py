import requests
import json
from typing import Optional


def get_summary(text: str)->Optional[str]:
    try:
        r = requests.post('https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict',
                          json={
                              "instances": [
                                {
                                  "text": text, "num_beams": 15,
                                  "num_return_sequences": 2,
                                  "length_penalty": 0.7
                                }
                              ]
                            })
        print(r.status_code)
        if r.status_code != 200:
            raise RuntimeError(f"Сбер вернул {r.status_code}")
        print(r.text)
        d = json.loads(r.text)
        return d['predictions']
    except Exception:
        return None


if __name__ == "__main__":
    print(get_summary("""ТАСС, 10 июня. Палеогенетики обнаружили в окрестностях кургана Телль-Карасса на юге Сирии древнее мусульманское захоронение c останками представителей Аравийского полуострова времен Дамасского халифата. Об этом в пятницу сообщила пресс-служба Шведского исследовательского совета (SRC).

Сирия и другие регионы Ближнего Востока стали частью Арабского халифата во времена правления первых халифов - сподвижников пророка Мухаммеда. В середине VII века они стали центром Дамасского халифата, первого крупного мусульманского государства в истории человечества. Его появление ассоциируется с формированием основ исламской культуры, законотворчества, финансов и других ключевых элементов цивилизации."""))