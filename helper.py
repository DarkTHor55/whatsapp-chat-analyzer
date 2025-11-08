from setuptools.command.rotate import rotate
from urlextract import URLExtract
import matplotlib.pyplot as plt
from  collections import Counter
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import emoji

def fetch_stats(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
    nums_message = df.shape[0]
    words = []
    num_media=df[df["message"]=="<Media omitted>\n"].shape[0]
    y=[]
    urlextract=URLExtract()
    for message in df['message']:
        words.extend(message.split())
        y.extend(urlextract.find_urls(message))
    return nums_message, words , num_media, len(y)

def groupby_stats(df):
    x = df['user'].value_counts().head()
    names = x.index
    counts = x.values
    percentage = (
        (df['user'].value_counts(normalize=True) * 100)
        .round(2)
        .reset_index()
    )
    percentage.columns = ['user', 'percent']

    fig1, ax1 = plt.subplots()
    ax1.bar(names, counts, color='skyblue')
    plt.xticks(rotation='vertical')
    plt.xlabel("Users")
    plt.ylabel("Messages")
    plt.title("Top 5 Most Active Users")


    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(
        percentage['percent'],
        labels=percentage['user'],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
        shadow=True
    )
    ax2.set_title("Message Contribution (%) by Users")
    ax2.axis('equal')

    return fig1, fig2, percentage

def create_wordCould(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    wc=WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    df_wc= wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_used_words(selected_user, df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df.dropna(subset=['message'])

    with open("stop_hinglish.txt", 'r', encoding='utf-8') as f:
        stop_words = f.read().split()

    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(10), columns=['Word', 'Count'])
    return return_df

def emoji_helper(selected_user, df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
      for c in message:
          if emoji.is_emoji(c):
              emojis.append(c)

    emoji_Counter=Counter(emojis)
    emoji_df=pd.DataFrame(emoji_Counter.most_common(len(emoji_Counter)), columns=['emoji','count'])
    return emoji_df

    
