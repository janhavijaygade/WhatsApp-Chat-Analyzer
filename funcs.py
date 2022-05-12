from urlextract import URLExtract
extract = URLExtract()
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user == 'Overall':
        # Counting number of messages
        num_messages = df.shape[0]

        # Counting number of words
        words = []
        for message in df['message']:
            words.extend(message.split())
        num_words = len(words)

        # Counting number of media files shared
        num_media_files = df[df['message'] == '<Media omitted>\n'].shape[0]

        # Counting number of links
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))
        num_links = len(links)
        return num_messages, num_words, num_media_files, num_links
    else:
        single_user_df = df[df['user'] == selected_user]
        # Counting number of messages
        num_messages = single_user_df.shape[0]

        # Counting number of words
        words = []
        for message in single_user_df['message']:
            words.extend(message.split())
        num_words = len(words)

        # Counting number of media files shared
        num_media_files = single_user_df[single_user_df['message'] == '<Media omitted>\n'].shape[0]

        # Counting number of links
        links = []
        for message in single_user_df['message']:
            links.extend(extract.find_urls(message))
        num_links = len(links)
        return num_messages, num_words, num_media_files, num_links

#function for busiest users
def most_busy_users(df):
    busy_users = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns = {'index':'name', 'user':'percent'}
    )
    return busy_users, df

#function for Most commonly used words(excluding the stop words)
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    #removing the group notifications
    temp_df = df[df['user'] != 'group_notification']
    #removing the media ommited messeges
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    words = []

    #importing stopwords file
    f= open('hinglish_stopwords.txt', 'r')
    stop_words_hinglish = f.read()

    #removing stopwords
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words_hinglish:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df

#function for Most commonly used emoji
def most_common_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    #extracting all emojis
    emojis =[]
    for message in df['message']:
        emojis.extend([e for e in message if e in emoji.UNICODE_EMOJI['en'] ])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return  emoji_df


#function for monthly timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_number', 'month']).count()['message'].reset_index()

    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

#function for daily timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    daily_timeline = df.groupby('date_for_timeline').count()['message'].reset_index()

    return daily_timeline

#function for Weekly timeline/activity
def weekly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    return  df['day_name'].value_counts()

#function for Monthly activity
def busy_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    return  df['month'].value_counts()

#Function for user activity throughout the day
def user_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    user_activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return  user_activity_heatmap
