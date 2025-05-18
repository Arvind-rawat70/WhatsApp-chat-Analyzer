import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor
from helper import (
    fetch_stats, most_busy_users, most_common_words,
    emoji_helper, monthly_timeline
)

st.sidebar.title("Whatsapp Chat Analyzer 📊")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats
        st.title("Top Statistics")
        num_messages, num_words, num_media, num_links = fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", num_words)
        col3.metric("Media Shared", num_media)
        col4.metric("Links Shared", num_links)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Most Active Users
        if selected_user == "Overall":
            st.title("Most Active Users")
            x, new_df = most_busy_users(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)

        # Most Common Words
        st.title("Most Common Words")
        most_common_df = most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'], color='blue')
        plt.xticks(rotation='horizontal')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = emoji_helper(selected_user, df)
        st.dataframe(emoji_df.head(10))
