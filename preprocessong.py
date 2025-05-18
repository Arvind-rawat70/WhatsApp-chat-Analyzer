import re
import pandas as pd

def preprocess(data):
    # Updated pattern: captures MM/DD/YY, time, AM/PM, user, message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s([APap][Mm])\s-\s(.*?):\s(.*)'
    matches = re.findall(pattern, data)

    if not matches:
        print("⚠️ No matches found — check the regex or input format.")

    # Build DataFrame
    df = pd.DataFrame(matches, columns=['date', 'time', 'ampm', 'user', 'message'])

    # Combine date and time strings
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'] + ' ' + df['ampm'], format='%m/%d/%y %I:%M %p')

    # Clean and rename
    df.drop(columns=['date', 'time', 'ampm'], inplace=True)
    df.rename(columns={'datetime': 'date'}, inplace=True)

    # Feature extraction
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['period'] = df['hour'].apply(lambda x: f'{x}-{x+1 if x < 23 else 0}')

    return df
