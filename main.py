import streamlit as st
import requests
import json
import pandas as pd
import time

st.markdown("![Alt Text](https://c.tenor.com/g5luJt5ki30AAAAC/fortune-teller-crystall-ball.gif)")
st.title('Topic Suggestions')


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


with st.form("my_form"):
    term = st.text_input('Enter a search term', placeholder='Online Poker')
    submitted = st.form_submit_button("Submit")


with st.form("bulk_submit"):
    bulk_term = st.file_uploader("Upload CSV Here",key=1)
    bulk_submitted = st.form_submit_button("Submit")
    my_bar = st.progress(0.0)
    my_bar_counter = 0.0

if submitted:
    download = []
    data = {}
    variations = ['what * ', 'is * ', 'who * ', 'how * ', 'does * ', 'why * ', 'can * ', 'where * ', 'when * ', '* ']
    for variant in variations:
        response = json.loads(
            requests.get(f'http://suggestqueries.google.com/complete/search?client=firefox&q={variant}{term}').text)
        data[response[0]] = [i for i in response[1]]
        time.sleep(0.1)

    for _, values in data.items():
        for value in values:
            download.append(value)

    df = pd.DataFrame({'suggest': download})
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'google_auto_suggest_{term}.csv',
        mime='text/csv',
    )

    for key, values in data.items():
        st.header(key.replace('*', '-'))
        for value in values:
            st.write(value)

if bulk_submitted:
    download = []
    data = {}
    variations = ['what * ', 'is * ', 'who * ', 'how * ', 'does * ', 'why * ', 'can * ', 'where * ', 'when * ', '* ']
    bulk_term_data = pd.read_csv(bulk_term,encoding='ascii',encoding_errors='replace')
    print(bulk_term_data.iloc[0:-1,0])
    api_progress_counter = 0

    for term in bulk_term_data.iloc[:,-1]:
        print(term)
        load_bar_integer = 1/len(bulk_term_data.index)
        my_bar_counter += load_bar_integer
        for variant in variations:
           if api_progress_counter == 50:
               time.sleep(6)
               api_progress_counter = 0

            response = json.loads(
                requests.get(f'http://suggestqueries.google.com/complete/search?client=firefox&q={variant}{term}').text)
            data[response[0]] = [i for i in response[1]]
            api_progress_counter += 1
            my_bar.progress(my_bar_counter+load_bar_integer)



    for _, values in data.items():
        for value in values:
            download.append(value)

    df = pd.DataFrame({'suggest': download})
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'google_auto_suggest_{term}.csv',
        mime='text/csv',
    )

    for key, values in data.items():
        st.header(key.replace('*', '-'))
        for value in values:
            st.write(value)

    st.balloons()