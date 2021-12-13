from enum import auto
from pandas.core.algorithms import isin
import streamlit as st
import pandas as pd
from components import *
from util import *
import nltk


nltk.download('punkt')

st.set_page_config(
    page_title='lexiscore',
    layout='wide',
    menu_items={
        'Get help': 'https://github.com/paulbricman/lexiscore/issues',
        'Report a Bug': 'https://github.com/paulbricman/lexiscore/issues/new',
        'About': 'https://paulbricman.com/thoughtware/lexiscore'
    })

sidebar_section()

if st.session_state['conceptarium_url'] == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    init()
    hero_section()

    col1, padding, col2 = st.columns([18, 1, 40])
    add_section(col1)
    cart_section(col2)
    meal_prep_section(col2)

    footer_section()
