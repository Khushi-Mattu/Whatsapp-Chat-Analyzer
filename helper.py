
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter


def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    #fetch no of messages
    num_messages=df.shape[0]

    from urlextract import URLExtract
    extractor = URLExtract()
    #fetch no of words
    words = []
    links=[]
    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))



    #fetch no of media_messages
    num_media=df[df['message']=='<Media omitted>\n'].shape[0]

    #fetch no of links shared
    num_links=len(links)


    return num_messages,len(words),num_media,num_links


def busiest_users(df):
    x = df['user'].value_counts().head()
    df = round(100 * (df['user'].value_counts().head() / df.shape[0]), 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc= WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # remove group notifications
    temp = df[df['user'] != 'group notification']

    # remove media omitted
    temp = temp[temp['message'] != '<Media omitted>\n']


    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    # remove stop words
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    from collections import Counter
    most_common_df=pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])


    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_time = df.groupby('only_date').count()['message'].reset_index()
    return daily_time


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap



