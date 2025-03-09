import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_ollama


st.title("AI web scrapper")

if "dom_content" not in st.session_state:
    st.session_state.dom_content = None

url = st.text_input("enter the url")

if st.button("scrape site"):
    st.write("scrapping the website")

    result= scrape_website(url)
    body_content= extract_body_content(result)
    clean_content = clean_body_content(body_content)
    
    st.session_state.dom_content = clean_content
    st.write("scrapping completed")

if st.session_state.dom_content:
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

    parse_description = st.text_area("Enter description for parsing")

    if st.button("parse_content"):
        if parse_description:
            st.write("parsing content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)

            st.session_state.parsed_result = result

            st.write(result)

# Display the parsed result persistently
if "parsed_result" in st.session_state:
    with st.expander("Parsed Result"):
        st.text_area("Parsed Content", st.session_state.parsed_result, height=300)  