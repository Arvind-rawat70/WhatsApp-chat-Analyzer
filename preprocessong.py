def preprocess(data):
    pattern = r'(\d{1,2})/(\d{1,2})/(\d{2}), (\d{1,2}):(\d{2})\s?(AM|PM)'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates_str = [
        f"{m.zfill(2)}/{d.zfill(2)}/{y.zfill(2)}, {h.zfill(2)}:{mi.zfill(2)} {ampm}"
        for m, d, y, h, mi, ampm in dates
    ]
    
    df = pd.DataFrame({'user_message': messages, 'message_date': dates_str})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Separate users and messages
    users = []
    messages_list = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # if there's a username
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])
    
    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)
    
    df['year'] = df['date'].dt.year
    df['months'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hours'] = df['date'].dt.hour
    df['mintues'] = df['date'].dt.minute
    
    return df
