from enum import auto
from pandas.core.algorithms import isin
import streamlit as st
from data import *
import pandas as pd
from components import *
from util import *


st.set_page_config(
    page_title='lexiscore',
    layout='wide',
    menu_items={
        'Get help': 'https://github.com/paulbricman/lexiscore/issues',
        'Report a Bug': 'https://github.com/paulbricman/lexiscore/issues/new',
        # TODO
        'About': 'https://paulbricman.com/thoughtware'
    })

sidebar_section()

if False:#st.session_state.conceptarium_url == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    purge_tmp()
    init()
    hero_section()

    col1, padding, col2 = st.columns([18, 1, 40])
    add_section(col1)
    cart_section(col2)
    meal_prep_section(col2)

    footer_section()
