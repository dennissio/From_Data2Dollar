# import libraries
import streamlit as st
import xgboost
import pandas as pd
import pickle
import os

st.write(os.getcwd())

# Load model
model = pickle.load(open("07_app/model.pkl", "rb"))

# Load dataset
df = pd.read_csv('07_app/xgb_data.csv')

# add logo
st.image('07_app/logo.png', width=300)

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
i = st.selectbox('City', df.columns[9:23])

#define values for prediction
def get_user_input(city):
    df_input = df.loc[df[city] == 1,:]
    df_model = df_input.mean()
    return df_model

#transpose data
df_model = get_user_input(i)
df_models = df_model.to_frame().transpose()
df_models['day'] = int(input_date[2])
df_models['month'] = int(input_date[1])
df_models['year'] = int(input_date[0])

# predict price
if st.button ('Predict Price'):
    X = df_models.drop('price', axis=1)
    prediction = model.predict(X)
    st.write('Predicted price CHF',prediction[0])
