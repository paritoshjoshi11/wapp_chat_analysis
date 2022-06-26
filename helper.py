from urlextract import URLExtract
from wordcloud import WordCloud 
import emoji
import pandas as pd
from collections import Counter

o=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # 1. Number of Messages    
    num_messages=df.shape[0]
    # 2. Number of words
    words=[]
    for i in df['message']:
        words.extend(i.split())
    
    # 3. Number of media messages
    num_media=df[df['message']=='<Media omitted>'].shape[0]

    # 4. Number of Links shared
    link=[]
    for i in df['message']:
        link.extend(o.find_urls(i))
    return num_messages,len(words),num_media,len(link)
    

def busy_user(df):
    n_df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return df['user'].value_counts().head(5),n_df

def wordcloud_f(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=' '))
    return df_wc   


# Emoji

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df