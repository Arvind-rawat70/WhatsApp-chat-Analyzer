import pandas as pd
from collections import Counter
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

extract = URLExtract()

# Fetching basic stats
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    num_words = sum(len(msg.split()) for msg in df['message'])
    num_media = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]
    links = [url for msg in df['message'] for url in extract.find_urls(msg)]

    return num_messages, num_words, num_media, len(links)

# Fetching the most active users
def most_busy_users(df):
    user_counts = df['user'].value_counts().head()
    percent_df = (df['user'].value_counts(normalize=True) * 100).round(2).reset_index()
    percent_df.columns = ['name', 'percent']
    return user_counts, percent_df

# Fetching the most common words
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    words = [word.lower() for msg in temp['message'] for word in msg.split() if word.lower() not in ENGLISH_STOP_WORDS]
    return pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])

# Emoji analysis
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['message'] != '<Media omitted>']
    emojis = [char for msg in df['message'] for char in msg if char in emoji.EMOJI_DATA]
    return pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])

# Generating wordcloud
def generate_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    words = ' '.join([word.lower() for msg in temp['message'] for word in msg.split() if word.lower() not in ENGLISH_STOP_WORDS])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)
    return wordcloud

# Monthly timeline for messages
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)
    return timeline
