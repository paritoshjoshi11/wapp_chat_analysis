import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.title('Whatsapp Chat Analyser')
st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode('utf-8')
     df=preprocessor.new(data)
     st.dataframe(df)

     # Fetch unique user
     userlist=df['user'].unique().tolist()
     userlist.remove('group_notification')
     userlist.sort()
     userlist.insert(0,'Overall')
     selected_user=st.sidebar.selectbox('Show analysis wrt ',userlist)
     if st.sidebar.button('Show Price Prediction') :
        num_messages,words,num_media,num_link=helper.fetch_stats(selected_user,df)
        st.title(selected_user)
        col1,col2,col3,col4=st.columns(4)
         
        with col1:
             st.header('Total Messages')
             
             st.title(num_messages)
        with col2:
             st.header('Total  Words')
             st.title(words)
        with col3:
             st.header('Media Shared')
             st.title(num_media)
        with col4:
             st.header('Link Shared')
             st.title(num_link)

        #  Finding busiest user in the group
        if(selected_user=='Overall'):
           
           st.title('Most Busy Users')
           x,n_df=helper.busy_user(df)
           col1,col2=st.columns(2)
           fig,ax=plt.subplots()
           with col1:
               ax.bar(x.index,x.values)
               plt.xticks(rotation='45')
               st.pyplot(fig)
           with col2:
               st.dataframe(n_df)


        #WORDCLOUD
        st.title('Most Used Words')
        df_wc=helper.wordcloud_f(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Emoji

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


               

            



    