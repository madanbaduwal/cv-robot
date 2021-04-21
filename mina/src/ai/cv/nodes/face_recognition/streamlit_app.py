# IN this model we create a simple web app. We take input from user(UI) and do prediction using src/models/predict_model.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src.models.predict_model import prediction1
import cv2

def app():
    """ Function that create web app"""

    # st.set_page_config(layout="wide")
    # st.title('Face recognition')


    # first_column, second_column= st.beta_columns(2)

    # with first_column:

    #     PERSON_GROUP_ID = st.text_input('Person group id')

    # with second_column:

    #     test_image_path = st.text_input('Url link')


    # with second_column:
    #     if st.button('Predict_'):
    #         name = prediction1(PERSON_GROUP_ID,test_image_path)
    #         st.write("The given face is of:",name)



    st.title("Webcam Live Feed")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    
    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')
app()


 
 # Writing explanation

# with st.beta_expander("See explanation"):
#      st.write("""
#          The chart above shows some numbers I picked for you.
#          I rolled actual dice for these, so they're *guaranteed* to
#          be random.
#      """)
#      st.image("https://static.streamlit.io/examples/dice.jpg")


# https://github.com/robmarkcole/mqtt-camera-streamer