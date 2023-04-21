import streamlit as st
import pandas as pd
import pickle

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Load the dataset
df = pd.read_csv('data_combined.csv')

# Function to predict the price
st.title('AirBnB Price Prediction')

# get user input