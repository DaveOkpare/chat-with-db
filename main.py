import re

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


def split_syntax(code):
    pattern = r"(\w+)\s*=\s*'([^']*)'"
    print(type(code))
    matches = re.findall(pattern, str(code))
    language_code_map = {language: value for language, value in matches}
    return language_code_map


def generate_response(prompt, languages):
    _schema = st.session_state['schema']
    db_url = st.session_state['database']
    _response = ask_ai(schema=_schema, prompt=prompt, database=db_url, languages=languages)
    return _response


with input_container:
    user_input = get_text()

with response_container:
    if user_input:
        options = st.multiselect('Choose your languages',
                                 ['SQL', 'Python', 'Golang', 'JavaScript', 'Dart'],
                                 None, )
        if options:
            syntax = generate_response(user_input, str(options))
            if syntax.sql:
                st.caption("SQL")
                st.code(syntax.sql, language="sql")
            if syntax.python:
                st.caption("Python")
                st.code(syntax.python, language="python")
            if syntax.javascript:
                st.caption("JavaScript")
                st.code(syntax.javascript, language="javascript")
            if syntax.golang:
                st.caption("Golang")
                st.code(syntax.golang, language="golang")
            if syntax.dart:
                st.caption("Dart")
                st.code(syntax.dart, language="dart")
