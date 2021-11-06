import streamlit as st


def hero_section():
    st.title('🥗 Shannon Nutri-Score')
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
        '📣 RSS (OPML)', '🔖 Bookmarks (HTML Export)', '📄 PDFs & 📕 EPUBs'))
    if type == '📣 RSS (OPML)' or type == '🔖 Bookmarks (HTML Export)':
        days = parent.number_input(
            'How many days does this stuff keep?', step=1)
    if type == '🔖 Bookmarks (HTML Export)':
        folder = parent.text_input('How\'s the bookmark folder called?')
    if type == '📄 PDFs & 📕 EPUBs':
        files = parent.file_uploader(
            'Place your food for thought here:', accept_multiple_files=True)
    else:
        files = parent.file_uploader(
            'Place your food for thought here:', accept_multiple_files=False)

    parent.caption('')
    if parent.button('add item'):
        if files == None:
            parent.warning('Please add file!')
        else:
            if not isinstance(files, list):
                files = [files]
            for file in files:
                new_entry = pd.DataFrame([[type, file.name, days, folder, file]], columns=[
                                         'type', 'filename', 'days', 'folder', 'file'])
                st.session_state['data'] = st.session_state['data'].append(
                    new_entry, ignore_index=True)

            st.experimental_rerun()


def basket_section(parent):
    parent.markdown('#### 🧺 basket')
    parent.markdown('')
    parent.table(st.session_state['data']
                 [['type', 'filename', 'days', 'folder']])
    parent.button('start labeling')

    parent.markdown('---')

    parent.markdown('#### 🍱 meal prep')
    parent.markdown('')
    parent.select_slider(
        'Specify the minimum Shannon Nutri-Score to use for meal prep:', ['A', 'B', 'C', 'D', 'E'])

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
