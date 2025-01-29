import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import mysql.connector

st.title('Upload your Business card')

uploaded_file = st.file_uploader('Browse a file') 

if uploaded_file is not None:
    st.write('Your file:', uploaded_file.name)

    image = Image.open(uploaded_file)
    st.image(image)

    image_np = np.array(image)

    reader = easyocr.Reader(['en'])
    detail = reader.readtext(image_np)

    edit_text=[]

    st.write('Check if your detail is right:')

    for index, detection in enumerate(detail, start=1):
     edited = st.text_input(f"Edit text: {index}: ", value=detection[1])
     edit_text.append(edited)
    
    if st.button('Save'):
        st.write('Edited_text: ')
        for idx, text in enumerate(edit_text, start=1):
            st.write(f"{idx}. {text}")

        def get_db_connection():
            connection = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'carolyn',
                database = 'bizcard_data',
            )
            return connection
 
        connection = get_db_connection()
        cursor = connection.cursor()

        for text in edit_text:
            cursor.execute('INSERT INTO bizcard_data(text) VALUES(%s)', (text,))
 

        connection.commit()
        cursor.close()
        connection.close()

        st.success('Success!')

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp{{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>

        """,
        unsafe_allow_html = True
    )
set_background('https://plus.unsplash.com/premium_photo-1661407772941-c5a2a5c9595b?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZGFyayUyMG9mZmljZXxlbnwwfHwwfHx8MA%3D%3D')