import streamlit as st
import pandas as pd
import pickle
import os

# Load the model
model = pickle.load(open("model.pkl", "rb"))

# Load the dataset
df = pd.read_csv('xgb_data.csv')

# add logo
st.image('logo.png', width=300)

# styling 
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        footer:after {
        content:'Made with love by: Deniz, Francesco, Manuel & Mathieu'; 
        visibility: visible;
        display: block;
        color: #25f5f3;
        }
        </style>
        """ 
st.markdown(hide_menu_style, unsafe_allow_html=True)

# get user input
date = st.date_input('Date')

#split date into day, month, year
input_date = str(date).split('-')

# get user input
i = st.selectbox('City', df.columns[15:29])

def get_user_input(city):
    df_input = df.loc[df[city] == 1,:]
    df_model = df_input.mean()
    return df_model

df_model = get_user_input(i)
df_models = df_model.to_frame().transpose()
df_models['day'] = int(input_date[2])
df_models['month'] = int(input_date[1])
df_models['year'] = int(input_date[0])

# get user input
if st.button ('Predict Price'):
    X = df_models.drop('price', axis=1)
    prediction = model.predict(X)
    st.write('Predicted price CHF',prediction[0])
