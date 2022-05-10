import streamlit as st
import requests
import json
import pandas as pd

st.markdown("![Alt Text](https://c.tenor.com/g5luJt5ki30AAAAC/fortune-teller-crystall-ball.gif)")
st.title('Topic Suggestions')


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


with st.form("my_form"):
    term = st.text_input('Enter a search term', placeholder='Online Poker')
    submitted = st.form_submit_button("Submit")

if submitted:
    download = []
    data = {}
    variations = ['what * ', 'is * ', 'who * ', 'how * ', 'does * ', 'why * ', 'can * ', 'where * ', 'when * ', '* ']
    for variant in variations:
        response = json.loads(
            requests.get(f'http://suggestqueries.google.com/complete/search?client=firefox&q={variant}{term}').text)
        data[response[0]] = [i for i in response[1]]

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
