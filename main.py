import streamlit as st
import preprocessor
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import funcs

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode("utf-8")
     #Getting data from preprocess function
     df = preprocessor.preprocess(data)

     #st.dataframe(df)

     #fetching all users
     userlist = df['user'].unique().tolist()
     if userlist == 'group_notification':
         userlist.remove('group_notification')
     userlist.sort()
     userlist.insert(0,"Overall")
     selected_user = st.sidebar.selectbox("Show analysis w.r.t. ", userlist)

    #Stats
     if st.sidebar.button("Show Analysis"):
         st.title("Top Statistics and Analysis")
         num_messages, num_words, num_media_files, num_links = funcs.fetch_stats(selected_user,df)
         col1, col2, col3,col4 = st.columns(4)
         with col1:
             st.header("Total messages")
             st.title(num_messages)
         with col2:
             st.header("Total words")
             st.title(num_words)
         with col3:
             st.header("Total media")
             st.title(num_media_files)
         with col4:
             st.header("Total links")
             st.title(num_links)

         #Busiest users
         if selected_user == 'Overall':
             st.title('Most Active Users')
             x, new_df = funcs.most_busy_users(df)
             col1, col2 = st.columns(2)

             with col1:
                 fig = px.bar(x=x.index, y=x.values, labels={"x":"User name", "y":"No. of messages"}, width=450, height=450)
                 #fig.show()
                 st.plotly_chart(fig)
             with col2:
                 st.header("Activity of all users(in %)")
                 st.dataframe(new_df)

         #Most commonly used words(excluding the stop words)
         st.title('Most Common Words')
         most_common_words_df = funcs.most_common_words(selected_user, df)
         #st.dataframe(most_common_words_df)
         fig = px.bar(x=most_common_words_df[1], y=most_common_words_df[0], labels={"x": "Occurence", "y": "Common Word"}, color=most_common_words_df[1], orientation='h')
         st.plotly_chart(fig)

         # Most commonly used emoji
         st.title('Emoji Analysis')
         emoji_df = funcs.most_common_emoji(selected_user, df)
         col1, col2 = st.columns([1,2])

         with col1:
             st.dataframe(emoji_df)

         with col2:
             fig = px.pie( values=emoji_df[1], names=emoji_df[0],
                          title='Emoji Analysis',
                          labels={'0': 'Emojis'})
             fig.update_traces(textposition='inside', textinfo='percent+label')
             st.plotly_chart(fig)

         #Monthly timeline
         st.title('Monthly timeline')
         timeline = funcs.monthly_timeline(selected_user, df)
         fig = px.line( x=timeline['time'], y=timeline['message'], labels={"x": "Timeline", "y": "No.of messages"})
         st.plotly_chart(fig)

         # Daily timeline
         st.title('Daily timeline')
         daily_timeline = funcs.daily_timeline(selected_user, df)
         fig = px.line(x=daily_timeline['date_for_timeline'], y=daily_timeline['message'], labels={"x": "Timeline", "y": "No.of messages"},)
         st.plotly_chart(fig)

         # Weekly timeline
         st.title('Weekly Analysis')
         busiest_week_day = funcs.weekly_timeline(selected_user, df)
         fig = px.bar(x=busiest_week_day.index, y=busiest_week_day.values, labels={"x": "Week day", "y": "No. of messages"}, color=busiest_week_day.values)
         st.plotly_chart(fig)

         # Busy month
         st.title('Monthly Analysis')
         busiest_month = funcs.busy_month(selected_user, df)
         fig = px.bar(x=busiest_month.index, y=busiest_month.values,
                      labels={"x": "Week day", "y": "No. of messages"}, color=busiest_month.values)
         st.plotly_chart(fig)

         # User activity heatmap
         st.title('User activity throughout the day')
         user_activity_heatmap = funcs.user_activity(selected_user, df)
         fig, r = plt.subplots()
         r = sns.heatmap(user_activity_heatmap, cmap='BuPu')
         st.write(fig)




