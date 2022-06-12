import streamlit as st
from annotated_text import annotated_text
import json

st.set_page_config(
   page_title="Fake Detection",
   page_icon="🤖",
    layout='wide'
)


# from config import sources
source_dict = {}

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

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys()\
            if i.startswith('dynamic_checkbox_') and st.session_state[i]]

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
        st.checkbox(i, key='dynamic_checkbox_' + i)


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

        if st.session_state['text'] and st.session_state['header']:
            button_container = st.empty()
            st.session_state['input_done'] = button_container.button('Проверить', disabled=False)

        if st.session_state['input_done']:
            st.session_state["active_sources"] = get_selected_checkboxes()
            text_input_container.empty()
            button_container.empty()

    with col2:
        st.header('Выберите источники')
        checkbox_container(sources)


def backend_connection():
    st.write('Выбраны: ', ', '.join(st.session_state['active_sources']))
    report = get_report(st.session_state['header'], st.session_state['text'], st.session_state['sources'])
    status = report['status']
    if status == 'not found':
        not_found_page(rep)
    elif status == 'with primary':
        with_primary_page(report)
    elif status == 'no primary':
        no_primary_page(rep)

def not_found_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        st.title('Ваш запрос')
        st.header(st.session_state['header'])
        st.text_area(label='Самари',
                     value ='samples' * 20,
                     height=300,
                     disabled=True)
    with col2:
        st.title('Не найдено')
        st.header(f'Достоверность : 0 %')
        st.markdown('Вердикт: *__не найдено__*')
        # парсинг

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

        # st.markdown(f"#### Кликбейтность {rep['clickbait']} %")
        # st.markdown(f"#### Сатиричность {rep['satirity']} %")
        st.metric(label="Кликбейтность", value=rep['clickbait'])
        st.metric(label="Сатиричность", value=rep['satirity'])
        st.markdown('_________________')

        col2.header(f'Источники:')

        for s in rep['sources']:
            if s['success'] == "True":
                st.markdown(f"### [{s['name']}](https://{s['url']})", unsafe_allow_html=True)
                annotate_text(s['result']['ner_content'])
            else:
                st.subheader(f'В {s["name"]} ничего не найдено')



def no_primary_page(rep):
    col1, col2 = st.columns((3, 3))
    with col1:
        #Hear we place user query title and NER from query content
        st.header('Ваш запрос')
        st.subheader(st.session_state['header'])
        annotate_text(rep['ner_content'])

    with col2:
        st.title('Искажение')
        st.header(f'Достоверность {rep["score"]} %')

        st.metric(label="Семантика", value=rep['semantic'], delta="1.2")
        st.metric(label="Тональность", value=rep['tonality'], delta="1.2")
        st.metric(label="Кликбейт", value=rep['clickbait'], delta="1.2")
        st.metric(label="Сатиричность", value=rep['satirity'], delta="1.2")

        for k, v in rep.items():
            if v['responce']:
                st.text_area(label=k,
                         value=f"{v['semant']}, {v['ton']}",
                         disabled=True)
                annotated_text("ПРИМЕР: ", ("Nemezida, Стартап, хакатон", "упоминается в обеих статьях"), "ЫЫЫ")
                annotated_text(("Инвестици, заказчики", "не упоминается в источнике"))
            else:
                st.text_area(label=k,
                             value=f"sample",
                             disabled=True)
input_page()
if st.session_state['input_done']:
    backend_connection()
