import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[apAP]\.?m\.?)?\s-\s'
    message = re.split(pattern, data)[1:]
    datas = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': message, 'message_date': datas})
    df['message_date'] = df['message_date'].apply(parse_date)
    df.rename({'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('user_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    return  df;





def parse_date(x):
    x = x.replace('\u202f', ' ').strip()
    if x.endswith('-'):
        x = x[:-1].strip()
    for fmt in ('%d/%m/%y, %I:%M %p', '%d/%m/%y, %H:%M'):
        try:
            return pd.to_datetime(x, format=fmt)
        except ValueError:
            continue
    return pd.NaT