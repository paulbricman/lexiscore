from enum import auto
from pandas.core.algorithms import isin
import streamlit as st
from data import *
import pandas as pd
from components import *


st.set_page_config(
    page_title='lexiscore',
    layout='wide',
    menu_items={
        # TODO
        #'Get help': 'https://github.com/paulbricman/shannon-nutri-score/issues',
        #'Report a Bug': 'https://github.com/paulbricman/shannon-nutri-score/issues/new',
        #'About': 'https://paulbricman.com/thoughtware/shannon-nutri-score'
    })

sidebar_section()

if False:#st.session_state.conceptarium_url == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    if 'data' not in st.session_state.keys():
       st.session_state['data'] = pd.DataFrame([], columns=['type', 'title', 'reading time', 'skill', 'challenge', 'lexiscore', 'text', 'raw', 'filename'])

    hero_section()

    col1, padding, col2 = st.columns([18, 1, 40])
    add_section(col1)
    cart_section(col2)

    footer_section()