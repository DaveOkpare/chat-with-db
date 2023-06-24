import openai
import streamlit as st

from utils import ask_ai, generate_schema

st.set_page_config(page_title="CodeBot - An LLM-powered Streamlit app to interact with database")

with st.sidebar:
    st.markdown("## SQL Repl")
    DATABASE_URL = st.text_input(
        "Connect to a database",
        placeholder="Enter DATABASE_URL"
    )
    OPENAI_API_KEY = st.text_input(
        "Bring your own :green[OPENAI_API_KEY]",
        type="password"
    )
    st.caption(':red[Disclaimer:] No API keys or database URLs are stored, they are only used '
               'during your current session.')

if st.sidebar.button("Submit"):
    if 'database' not in st.session_state:
        st.session_state['database'] = DATABASE_URL
    st.session_state['database'] = DATABASE_URL

    if 'key' not in st.session_state:
        st.session_state['key'] = OPENAI_API_KEY
    st.session_state['key'] = OPENAI_API_KEY

    if 'schema' not in st.session_state:
        st.session_state['schema'] = generate_schema(DATABASE_URL)
    st.session_state['schema'] = generate_schema(DATABASE_URL)

    openai.api_key = OPENAI_API_KEY

st.sidebar.markdown("###### [Source Code](https://google.com)")

input_container = st.container()
response_container = st.container()


def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


def generate_response(prompt, languages):
    _schema = st.session_state['schema']
    db_url = st.session_state['database']
    _response = ask_ai(_schema, prompt, db_url)
    return _response


with input_container:
    user_input = get_text()

with response_container:
    if user_input:
        syntax, description = generate_response(user_input)
        st.code(syntax[1], language="sql")
        st.markdown(description[1])
