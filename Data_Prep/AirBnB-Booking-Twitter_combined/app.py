import streamlit as st
import pandas as pd
import pickle

# Load the model
model = pickle.load(open('model.pkl', 'rb'))


# Load the dataset
df = pd.read_csv('xgb_data.csv')

# Function to predict the price
st.title('AirBnB Price Prediction')

# get user input
st.date_input('Date')

# get user input
i = st.selectbox('City', df.columns[15:29])

def get_user_input(city):
    df_input = df.loc[df[city] == 1,:]
    df_model = df_input.mean()
    return df_model

df_model = get_user_input(i)
df_models = df_model.to_frame().transpose()
# get user input
if st.button ('Predicted Price'):
    X = df_models.drop('price', axis=1)
    prediction = model.predict(X)
    st.write('Predicted price CHF',prediction[0])
