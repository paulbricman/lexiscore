from numpy.lib.function_base import select
from reportlab.platypus.flowables import PageBreak
import streamlit as st
import pandas as pd
from connectors import *
import time
import numpy as np
from processing import *
from util import *
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import webbrowser
import pathlib


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

                with st.spinner('Fetching content...'):
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
                    if len(v[0].split()) / 250 > 1:
                        new_entry = pd.DataFrame([[item_type, k, round(len(v[0].split()) / 250), 'N/A', 'N/A', 'N/A', v[0], v[1], v[2]]], columns=['type', 'title', 'reading time', 'skill', 'challenge', 'lexiscore', 'text', 'raw', 'filename'])
                        st.session_state['data'] = st.session_state['data'].append(
                            new_entry, ignore_index=True)

            st.experimental_rerun()


def cart_section(parent):
    parent.markdown('#### 🛒 cart')
    parent.markdown('')
    parent.table(st.session_state['data'][['type', 'title', 'reading time', 'skill', 'challenge', 'lexiscore']])
    
    if st.session_state['data'].shape[0] > 0:
        parent.caption('Total reading time: ' + str(round(sum(st.session_state['data'][['reading time']].values)[0])) + ' minutes')
        if parent.button('start labeling'):
            with st.spinner('Warming up NLP models...'):
                encoder_model = init_encoder()
                autoregressive_model = init_autoregressive()
                tokenizer = init_tokenizer()

                conceptarium = fetch_conceptarium()
                conceptarium = [e['content'] for e in conceptarium if e['modality'] == 'language']
                conceptarium_embeddings = get_embeddings(encoder_model, conceptarium)

            for idx, row in st.session_state['data'].iterrows():
                with st.spinner('Determining the nutritional value of "' + row['title'] + '"...'):
                    content_paragraphs = get_paragraphs(row['text'])
                    content_embeddings = get_embeddings(encoder_model, content_paragraphs)
                

                    if len(content_paragraphs) > 1 and len('\n\n'.join(content_paragraphs).split()) > 150:
                        results = get_closest_thoughts(conceptarium_embeddings, content_embeddings)
                        skill = get_skill(results)
                        challenge = get_challenge(conceptarium, results, content_paragraphs, autoregressive_model)
                        raw_challenge = get_raw_challenge(content_paragraphs, autoregressive_model)
                        challenge = -(raw_challenge - challenge) / raw_challenge

                        alpha = np.arctan((challenge + 0.2) / (skill - 0.2))
                        lexiscore = np.abs(alpha - 0.6) // (0.35 / 2)

                        if lexiscore >= 4:
                            lexiscore = 'E'
                        elif lexiscore == 3:
                            lexiscore = 'D'
                        elif lexiscore == 2:
                            lexiscore = 'C'
                        elif lexiscore == 1:
                            lexiscore = 'B'
                        else:
                            lexiscore = 'A'

                        st.session_state['data'].loc[idx]['skill'] = skill
                        st.session_state['data'].loc[idx]['challenge'] = challenge
                        st.session_state['data'].loc[idx]['lexiscore'] = lexiscore

                        print(st.session_state['data'][['skill', 'challenge', 'lexiscore']])
                    else:
                        print('no paragraphs:', row['title'], '---', row['text'], '---')
            
            st.experimental_rerun()
        
        if not 'N/A' in st.session_state['data']['lexiscore'].values:
            
            parent.markdown('---')
            parent.markdown('#### 📈 distribution')
            fig = px.scatter(st.session_state['data'], x='skill', y='challenge', hover_data=['title', 'lexiscore'], color_discrete_sequence=['#228b22'])
            
            parent.plotly_chart(fig)



def meal_prep_section(parent):
    if st.session_state['data'].shape[0] > 0 and not 'N/A' in st.session_state['data']['lexiscore'].values:
        parent.markdown('---')
        parent.markdown('#### 🍱 meal prep')
        parent.markdown('')
        lexiscores = ['A', 'B', 'C', 'D', 'E']
        min_lexiscore = parent.select_slider(
            'Specify the minimum lexiscore to use for meal prep:', lexiscores)
        allowed_lexiscores = lexiscores[:lexiscores.index(min_lexiscore) + 1]

        if parent.button('start'):
            selection = [e in allowed_lexiscores for e in st.session_state['data']['lexiscore']]
            selection = st.session_state['data'][selection]

            if selection.shape[0] == 0:
                parent.warning('No item qualifies for this selection, please lower the bar!')
            else:
                html = '<h1>🍱 meal prep</h1><hr><div><br/><br/></div>'

                for idx, row in selection.iterrows():
                    html += '<h1>🥗 ' + row['title'] + '</h1>'
                    html += '<li><b>⏱️ ' + str(row['reading time']) + '</b> minutes</li>'
                    html += '<li>📗 lexiscore <b>' + row['lexiscore'] + '</b></li>'
                    html += '<hr><div><br/><br/></div>'
                    
                    if row['type'] != '📄 PDF':
                        html += row['raw']
                    else:
                        pix_paths = pdf_to_images(row['filename'])
                        
                        for pix_path in pix_paths:
                            html += '<img src="file://' + os.path.abspath(pix_path) + '"><br/>'
                    
                    html += '<div><br/><br/></div><hr>'
                
                f = open(os.path.abspath('tmp/mealprep.html'), 'w+')
                f.write(html)
                
                parent.info('Meal prep complete! Please use the button below to download the results.')
                parent.download_button(label='download', data=html, file_name='mealprep.html', mime='text/html')
        

def footer_section():
    st.markdown('---')
    st.markdown('')
    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

'''
>>> data['lexiscore'] = np.abs(data['alpha']-0.6) // (np.std(data['alpha'] / 2))
>>> px.scatter(data, x='skill', y='challenge', hover_data=['title', 'lexiscore']).show()
'''