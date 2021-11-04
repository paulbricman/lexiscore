from enum import auto
from pandas.core.algorithms import isin
import streamlit as st
from data import *
import pandas as pd


st.set_page_config(
    page_title='shannon score',
    layout='wide',
    menu_items={
        'Get help': 'https://github.com/paulbricman/shannon-nutri-score/issues',
        'Report a Bug': 'https://github.com/paulbricman/shannon-nutri-score/issues/new',
        'About': 'https://paulbricman.com/thoughtware/shannon-nutri-score'
    })

st.sidebar.header('settings')
st.session_state.conceptarium_url = st.sidebar.text_input('What\'s the URL of your conceptarium?')

if False:#st.session_state.conceptarium_url == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    st.title('🍏 Shannon Nutri-Score')
    st.markdown('A nutritional label for food for thought.')


    st.markdown('---')
    col1, padding, col2 = st.columns([30, 1, 20])

    if 'data' not in st.session_state.keys():
       st.session_state['data'] = pd.DataFrame([], columns=['type', 'filename', 'days', 'folder', 'file'])


    col1.markdown('#### ➕ add source')

    days = None
    folder = None

    type = col1.selectbox('What type of source would you like to add?', ('📣 RSS (OPML)', '🔖 Bookmarks (HTML Export)', '📄 PDFs & 📕 EPUBs'))
    if type == '📣 RSS (OPML)' or type == '🔖 Bookmarks (HTML Export)':
        days = col1.number_input('How many days does this keep?', step=1)
    if type == '🔖 Bookmarks (HTML Export)':
        folder = col1.text_input('What\'s the bookmark folder exactly?')
    if type == '📄 PDFs & 📕 EPUBs':
        files = col1.file_uploader('Place your food for thought in here:', accept_multiple_files=True)
    else:
        files = col1.file_uploader('Place your food for thought in here:', accept_multiple_files=False)


    col1.caption('')
    if col1.button('add source'):
        if files == None:
            col1.warning('Please add file!')
        else:
            if not isinstance(files, list):
                files = [files]
            for file in files:
                print('working on:', file.name)
                new_entry = pd.DataFrame([[type, file.name, days, folder, file]], columns=['type', 'filename', 'days', 'folder', 'file'])
                #table.add_rows(new_entry[['type', 'filename', 'days', 'folder']])
                st.session_state['data'] = st.session_state['data'].append(new_entry, ignore_index=True)
                #print(st.session_state['data'])
            st.experimental_rerun()
    
    col2.markdown('#### 🧺 sources')
    col2.markdown('')
    col2.table(st.session_state['data'][['type', 'filename', 'days', 'folder']])
    col2.button('start labeling')

    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)