import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

import preprocessor
import helper



st.sidebar.title("Whatsapp Chat Analyzer")
upload_file=st.sidebar.file_uploader("choose a file")
if upload_file is not None:
    byte_data=upload_file.getvalue()
    data=byte_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    st.dataframe(df)
    user_list=df["user"].unique().tolist()
    user_list.remove('user_notification')
    user_list.sort()
    user_list.insert(0,"OverAll")

    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show Analyze"):
        num_messages,words,num_media, y=helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 =st.columns(4)

        with col1:
            st.write("Total Message")
            st.title(num_messages)
        with col2:
            st.write("Total words")
            st.title(len(words))
        with col3:
            st.write("Total Media")
            st.title(num_media)
        with col4:
            st.write("Total Links")
            st.title(y)

        # most actve user in group
        if selected_user == "OverAll":
            st.title("Most Active Users")

            bar_fig, pie_fig, percentage = helper.groupby_stats(df)

            col1, col2 ,col3= st.columns(3)

            with col1:
                st.subheader("Top 5 Active Users (Bar Chart)")
                st.pyplot(bar_fig)

            with col2:
                st.subheader("User Message Share (%) (Pie Chart)")
                st.pyplot(pie_fig)

            with col3:
                st.subheader("User Contribution Table")
                st.dataframe(percentage)

    st.title("Word Cloud")
    df_wc=helper.create_wordCould(selected_user, df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.title("Most Comman words")
    most_comman_df= helper.most_used_words(selected_user, df)
    fig,ax=plt.subplots()
    ax.barh(most_comman_df['Word'], most_comman_df['Count'])
    plt.xticks(rotation=90)

    st.pyplot(fig)

    st.title("Emoji Analysis")
    emojis=helper.emoji_helper(selected_user, df)

    col1,col2 =st.columns(2)
    with col1:
        st.write("Emoji DataFrame")
        st.dataframe(emojis)
    with col2:
        st.write("Emoji PieChart")
        if not emojis.empty:
            top_emojis = emojis.head(10)
            fig, ax = plt.subplots()

            ax.pie(
                top_emojis['count'],
                labels=top_emojis['emoji'],
                autopct='%1.1f%%',
                startangle=90,
                wedgeprops={'edgecolor': 'black'}
            )

            ax.set_title("Top 10 Emojis Used")
            st.pyplot(fig)
        else:
            st.warning("No emojis found in chat.")









