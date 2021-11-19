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
        'Get help': 'https://github.com/paulbricman/lexiscore/issues',
        'Report a Bug': 'https://github.com/paulbricman/lexiscore/issues/new',
        # TODO
        'About': 'https://paulbricman.com/thoughtware'
    })

sidebar_section()

if False:#st.session_state.conceptarium_url == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    if 'data' not in st.session_state.keys():
        st.session_state['data'] = pd.DataFrame([], columns=['type', 'title', 'reading time', 'skill', 'challenge', 'lexiscore', 'text', 'raw', 'filename'])
    if 'encoder_model' not in st.session_state.keys():
        with st.spinner('Loading encoder model for finding notes related to content...'):
            st.session_state['encoder_model'] = init_encoder()
    if 'autoregressive_model' not in st.session_state.keys():
        with st.spinner('Loading autoregressive model for reconstructing content...'):
            st.session_state['autoregressive_model'] = init_autoregressive()
    if 'tokenizer' not in st.session_state.keys():
        with st.spinner('Loading tokenizer...'):
            st.session_state['tokenizer'] = init_tokenizer()
    if 'conceptarium' not in st.session_state.keys():
        with st.spinner('Loading conceptarium and encoding it in advance...'):
            conceptarium = fetch_conceptarium()
            conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
            conceptarium_embeddings = get_embeddings(conceptarium)
            st.session_state['conceptarium'] = conceptarium
            st.session_state['conceptarium_embeddings'] = conceptarium_embeddings

    hero_section()

    col1, padding, col2 = st.columns([18, 1, 40])
    add_section(col1)
    cart_section(col2)
    meal_prep_section(col2)

    footer_section()
