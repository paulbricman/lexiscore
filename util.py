import json
import fitz
import os
import streamlit as st
from processing import *
import pandas as pd
import requests


def fetch_conceptarium():
    conceptarium_url = st.session_state['conceptarium_url']
    if not conceptarium_url.startswith('http://'):
        conceptarium_url = 'http://' + conceptarium_url
    if conceptarium_url[-1] == '/':
        conceptarium_url = conceptarium_url[:-1]

    conceptarium_url += '/find'
    conceptarium = requests.get(conceptarium_url, params={
        'query': '',
        'return_embeddings': False
    }, headers={
        'authorization': 'Bearer ' + st.session_state['access_token']
    }).json()
    return conceptarium


def pdf_to_images(path):
    doc = fitz.open(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    pix_paths = []

    for page_idx, page in enumerate(doc.pages()):
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))
        pix_path = os.path.abspath(
            './tmp/' + filename + str(page_idx) + '.png')
        pix_paths += [pix_path]
        pix.save(pix_path)

    return pix_paths


def purge_tmp():
    for root, dirs, files in os.walk('tmp'):
        for file in files:
            os.remove(os.path.abspath(os.path.join(root, file)))


def init():
    if 'data' not in st.session_state.keys():
        st.session_state['data'] = pd.DataFrame([], columns=[
                                                'type', 'title', 'reading time', 'skill', 'challenge', 'lexiscore', 'text', 'raw', 'filename'])
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
            conceptarium = fetch_conceptarium()['authorized_thoughts']
            conceptarium = [e['content']
                            for e in conceptarium if e['modality'] == 'text']
            conceptarium_embeddings = get_embeddings(conceptarium)
            st.session_state['conceptarium'] = conceptarium
            st.session_state['conceptarium_embeddings'] = conceptarium_embeddings
