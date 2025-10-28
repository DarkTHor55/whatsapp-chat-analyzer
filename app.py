import streamlit as st
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
        num_messages=helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 =st.columns(4)

        with col1:
            st.write("Total Message")
            st.title(num_messages)
        with col2:
            st.write("Column 2")
        with col3:
            st.write("Column 3")
        with col4:
            st.write("Column 4")

