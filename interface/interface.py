import streamlit as st
from annotated_text import annotated_text
import json

st.set_page_config(
   page_title="Fake Detection",
   page_icon="🤖",
    layout='wide'
)


# from config import sources
source_dict = {
'interfax.ru': 'Интерфакс',
'nauka.tass.ru': 'ТАСС',
'mos.ru' : 'Mos.ru',
# 'www.mos.ru/news/item/' : 'Mos.ru',
'/www.kommersant.ru/': 'Коммерсант',
'https://lenta.ru/news/': 'Лента',
'rbk.ru' : 'РБК'
}

def annotate_text(ner):
    text = [tuple(i) if type(i) == list else i for i in ner]
    annotated_text(*text)

if 'sources' not in st.session_state.keys():
    sources = ['Интерфакс', 'РБК', 'Mos.ru', 'Коммерсант', 'Лента', 'ТАСС']
    st.session_state['sources'] = sources
else:
    sources = st.session_state['sources']

def get_report(header, text, sources):
    json_path = "./back_result.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        result = json.loads(f.read())
    return result



def checkbox_container(data):
    if st.button('Выбрать все'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        st.experimental_rerun()
    if st.button('Очистить'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        st.experimental_rerun()
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i, value=1)

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys()\
            if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def get_selected_urls(names):
    result = []
    for k, v in source_dict.items():
        if v in names:
            result.append(k)
    return result


def input_page():
    st.session_state['input_done'] = False
    col1, col2 = st.columns((3, 1))
    with col1:
        st.header('Введите данные')
        header = st.text_input(label='Заголовок',
                               max_chars=200,
                               key=2
                               )
        st.session_state['header'] = header

        text_input_container = st.empty()
        text = text_input_container.text_area(label='Текст',
                                              height=300,
                                              key=3
                                              )

        st.session_state['text'] = text


        if st.session_state['text'] and st.session_state['header'] and st.session_state["active_sources"]:
            button_container = st.empty()
            st.session_state['input_done'] = button_container.button('Проверить', disabled=False)

        if st.session_state['input_done']:
            st.session_state["active_sources"] = get_selected_checkboxes()
            st.write('select')
            st.session_state["active_urls"] = get_selected_urls(st.session_state["active_sources"])

            text_input_container.empty()
            button_container.empty()

        if st.session_state['input_done'] == False:
            with col2:
                st.header('Выберите источники')
                checkbox_container(sources)
                st.session_state["active_sources"] = get_selected_checkboxes()
        else:
            with col2:
                # кнопка ввести новую статью
                pass

def backend_connection():
    st.markdown('##### Выбраны: ' + ', '.join(st.session_state['active_sources']))
    report = get_report(st.session_state['header'], st.session_state['text'], st.session_state['sources'])
    status = report['status']
    if status == 'not found':
        not_found_page(report)
    elif status == 'with primary':
        with_primary_page(report)
    elif status == 'no primary':
        no_primary_page(report)



def with_primary_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        st.header('Ваш запрос')
        st.markdown(f"#### {st.session_state['header']}")
        annotate_text(rep['ner_content'])

        #Hear we place primary of query and it's summary
        primary = rep['sources'][0]
        st.markdown(f"#### Первоисточник: [{primary['name']}](https://{primary['url']})")
        annotate_text(primary['result']['ner_content'])

    with col2:
        col2.header(f'Достоверность {rep["score"]} %')
        col2.markdown(f"### Вердикт: *__перефразировано__*")

        st.metric(label="Кликбейтность", value=rep['clickbait'])
        st.metric(label="Сатиричность", value=rep['satirity'])
        st.markdown('_________________')

        col2.header(f'Источники:')

        for s in rep['sources']:
            if s['success'] == "True" and s["name"] in st.session_state["active_urls"]:
                st.markdown(f"### Найдено: [{s['name']}](https://{s['url']})", unsafe_allow_html=True)
                annotate_text(s['result']['ner_content'])
                st.markdown('###### В обеих статьях упоминаются:')
                annotate_text(s['result']['ner_inter'])
                st.markdown('###### В источнике не говорится о:')
                annotate_text(s['result']['ner_add'])

            elif s['success'] == "False" and s["name"] in st.session_state["active_urls"]:
                st.subheader(f'В {s["name"]} ничего не найдено')




def no_primary_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        col1.header('Ваш запрос')
        col1.markdown(f"#### {st.session_state['header']}")
        annotate_text(rep['ner_content'])

    with col2:
        col2.header(f'Достоверность {rep["score"]} %')
        col2.markdown(f"### Вердикт: *__искажение__*")
        st.metric(label="Кликбейтность", value=rep['clickbait'])
        st.metric(label="Сатиричность", value=rep['satirity'])
        st.markdown('_________________')

        col2.header(f'Источники:')

        for s in rep['sources']:
            if s['success'] == "True" and s["name"] in st.session_state["active_urls"]:
                st.markdown(f"### Схожесть {s['result']['semantic']} % c [{s['name']}](https://{s['url']})", unsafe_allow_html=True)
                annotate_text(s['result']['ner_content'])
                st.markdown('###### В обеих статьях упоминаются:')
                annotate_text(s['result']['ner_inter'])
                st.markdown('###### В источнике не говорится о:')
                annotate_text(s['result']['ner_add'])

            elif s['success'] == "False" and s["name"] in st.session_state["active_urls"]:
                st.subheader(f'В {s["name"]} ничего не найдено')

def not_found_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        col1.header('Ваш запрос')
        col1.markdown(f"#### {st.session_state['header']}")
        annotate_text(rep['ner_content'])

    with col2:
        col2.header(f'Достоверность {rep["score"]} %')
        col2.markdown(f"### Вердикт: *не найдено*")
        st.metric(label="Кликбейтность", value=rep['clickbait'])
        st.metric(label="Сатиричность", value=rep['satirity'])
        st.markdown('_________________')

input_page()
if st.session_state['input_done']:
    backend_connection()
