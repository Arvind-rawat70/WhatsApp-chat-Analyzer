import streamlit as st

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.write("Upload a file below:")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    st.text(data)
