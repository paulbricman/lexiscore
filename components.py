import streamlit as st
import pandas as pd
from connectors import *
import time
import numpy as np


def hero_section():
    st.title('📗 lexiscore')
    st.markdown('A nutritional label for food for thought.')
    st.markdown('---')


def sidebar_section():
    st.sidebar.header('settings')
    st.session_state.conceptarium_url = st.sidebar.text_input(
        'What\'s the URL of your conceptarium?')


def add_section(parent):
    parent.markdown('#### ➕ add food for thought')

    days = None
    folder = None

    type = parent.selectbox('What type of food for thought would you like to add?', (
        '📣 RSS (OPML)', '🔖 Bookmarks (HTML Export)', '📄 PDF', '📕 EPUB', '📝 Plain Text'))

    if type == '📣 RSS (OPML)':
        days = parent.number_input(
            'How many days does this stuff keep?', step=1)
        files = parent.file_uploader(
            'Place your food for thought here:', type=['xml', 'opml'])
    elif type == '🔖 Bookmarks (HTML Export)':
        folder = parent.text_input('How\'s the bookmark folder called?')
        days = parent.number_input(
            'How many days does this stuff keep?', step=1)
        files = parent.file_uploader(
            'Place your food for thought here:', type=['html'])
    elif type == '📄 PDF':
        files = parent.file_uploader(
            'Place your food for thought here:', accept_multiple_files=True, type='pdf')
    elif type == '📕 EPUB':
        files = parent.file_uploader(
            'Place your food for thought here:', accept_multiple_files=True, type='epub')
    elif type == '📝 Plain Text':
        files = parent.file_uploader(
            'Place your food for thought here:', accept_multiple_files=True, type=['text', 'txt', 'md'])

    parent.caption('')

    if parent.button('add item'):
        if files == None:
            parent.warning('Please add file!')
        else:
            if not isinstance(files, list):
                files = [files]

            for file in files:
                f = open(os.path.join('tmp', file.name), 'wb+')
                f.write(file.getbuffer())
                f.close()

                path = os.path.join('tmp', file.name)

                if type == '📣 RSS (OPML)':
                    item_type = '📣 RSS'
                    data = fetch_from_opml(path, days)
                elif type == '🔖 Bookmarks (HTML Export)':
                    item_type = '🔖 Bookmark'
                    data = fetch_from_bookmarks(path, folder, days)
                elif type == '📄 PDF':
                    item_type = '📄 PDF'
                    data = fetch_from_pdf(path)
                elif type == '📕 EPUB':
                    item_type = '📕 EPUB'
                    data = fetch_from_epub(path)
                elif type == '📝 Plain Text':
                    item_type = '📝 Plain Text'
                    data = fetch_from_plaintext(path)

                for k, v in data.items():
                    new_entry = pd.DataFrame([[item_type, k, round(len(v.split()) / 250), v]], columns=['type', 'title', 'reading time', 'text'])
                    st.session_state['data'] = st.session_state['data'].append(
                        new_entry, ignore_index=True)

                os.remove(path)

            st.experimental_rerun()


def cart_section(parent):
    parent.markdown('#### 🛒 cart')
    parent.markdown('')
    parent.table(st.session_state['data'][['type', 'title', 'reading time']])
    
    if st.session_state['data'].shape[0] > 0:
        parent.caption('Total: ' + str(sum(st.session_state['data'][['reading time']].values)[0]) + ' minutes')
    parent.button('start labeling')

    parent.markdown('---')

    parent.markdown('#### 🍱 meal prep')
    parent.markdown('')
    parent.select_slider(
        'Specify the minimum lexiscore to use for meal prep:', ['A', 'B', 'C', 'D', 'E'])

    parent.button('generate epub')
    parent.button('generate pdf')


def footer_section():
    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
