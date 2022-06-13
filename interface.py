import streamlit as st
from annotated_text import annotated_text
import json


from backend import check_news
from cfg import *

st.set_page_config(
   page_title="Fake Detection",
   page_icon="🤖",
    layout='wide'
)
TEST_MODE = False

# from config import sources
source_dict = {
    'interfax.ru': 'Интерфакс',
    'nauka.tass.ru': 'ТАСС',
    'mos.ru': 'Mos.ru',
    'kommersant.ru': 'Коммерсант',
    'lenta.ru': 'Лента',
    'rbc.ru': 'РБК'
}

if 'sources' not in st.session_state.keys():
    sources = ['Интерфакс', 'РБК', 'Mos.ru', 'Коммерсант', 'Лента', 'ТАСС']
    st.session_state['sources'] = sources
else:
    sources = st.session_state['sources']

def checkbox_container(data):
    """
    Creates multiple checkboxes for setting sources
    :param data: sources list
    """
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
    """
    :return: chosen sources in checbox_container for current moment
    """
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys()\
            if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def get_selected_urls(names):
    """
    :param names: sources:
    :return: urls for current sources
    """
    result = []
    for k, v in source_dict.items():
        if v in names:
            result.append(k)
    return result

def annotate_text(ner):
    """
    Place annotated text
    :param ner: list of strings with annotations
    """
    text = []

    for i in ner:
        if type(i) == list:
            i[0] = i[0].replace('-', ' ') + ' '
            text.append(tuple(i))
        elif type(i) == str:
            i = i.replace('-', ' ') + ' '
            text.append(i)

    annotated_text(*text)

def annotate_ners(ner, flg):
    """
    Place annotated NERS
    :param flg: True in itersection else False
    :param ner: list of strings with annotations
    """
    text = ''
    for i in ner:
        text += i + ' '
    if flg:
        annotated_text((text, 'совпали'))
    else:
        annotated_text((text, 'остутствуют'))

def get_report(title, content, sources, test_mode=False):
    """
    :param title: article title
    :param content: article content
    :param sources: chosen sources
    :param test_mode: test mode flag
    :return: query result from back for current article
    """
    if test_mode:
        # json_path = "./interface/back_result.json"
        # with open(json_path, 'r', encoding='utf-8') as f:
        #     response = json.loads(f.read())
        # return response
        return test_response
    response = check_news(title, content, sources)
    return response

def article_stats(rep):
    """
    Shows main stats for article
    :param rep: query result from back for current article
    """
    if rep["score"] > score_thr:
        ans = "Перефразировано"
    elif rep["score"] == 0:
        ans = "Не найдено"
    else:
        ans = "Искажено"

    st.header(f'Достоверность {rep["score"]} %')
    st.markdown(f"### Вердикт: *__{ans}__*")

    st.metric(label="Кликбейтность", value=rep['clickbait'])
    # st.metric(label="Сатиричность", value=rep['satirity'])
    st.markdown('_________________')

def sources_stats(rep):
    """
    Shows stats for found sources
    :param rep: query result from back for current article
    """
    st.header(f'Источники:')

    for s in rep['sources']:
        if s['success'] and s["name"] in st.session_state["active_urls"]:
            st.markdown(f"### Найдено: [{s['name']}]({s['url']})", unsafe_allow_html=True)
            st.markdown(f"#### Схожесть: {s['result']['semantic']}")
            st.markdown(f"#### Кликбейтность: {s['result']['clickbait']}")
            st.markdown('#### В обеих статьях упоминаются:')
            annotate_ners(s['result']['ner_inter'], True)
            st.markdown('#### В источнике не говорится о:')
            annotate_ners(s['result']['ner_add'], False)


def input_page():
    """
    Func for showing input page of app
    """
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
            # st.write('select')
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
    """
    Provide article information to back, show answer page for given article
    :return:
    """
    st.markdown('##### Выбраны: ' + ', '.join(st.session_state['active_sources']))
    report = get_report(st.session_state['header'], st.session_state['text'], st.session_state['active_urls'], test_mode=TEST_MODE)
    status = report['status']
    if status == NOT_FOUND:
        not_found_page(report)
    elif status == WITH_PRIMARY:
        with_primary_page(report)
    elif status == NO_PRIMARY:
        no_primary_page(report)



def with_primary_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        col1.header('Ключевые упоминания')
        # col1.markdown(f"#### {st.session_state['header']}")
        col1.markdown(f"#### Ваш запрос")
        annotate_text(rep['ner_content'])

        #Hear we place primary of query and it's summary
        primary = rep['sources'][0]
        st.markdown(f"#### Первоисточник: [{primary['name']}]({primary['url']})")
        annotate_text(primary['result']['ner_content'])

    with col2:
        article_stats(rep)
        sources_stats(rep)




def no_primary_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        col1.header('Ваш запрос')
        col1.markdown(f"#### {st.session_state['header']}")
        annotate_text(rep['ner_content'])

    with col2:
        article_stats(rep)
        sources_stats(rep)


def not_found_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        col1.header('Ваш запрос')
        col1.markdown(f"#### {st.session_state['header']}")
        annotate_text(rep['ner_content'])

    with col2:
        article_stats(rep)

input_page()
if st.session_state['input_done']:
    backend_connection()
