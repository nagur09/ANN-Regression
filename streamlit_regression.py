import streamlit as st
import numpy as np 
import pandas as pd
import tensorflow as tf
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

#load the trained model

model = tf.keras.models.load_model('regression_model.h5')

# Load the encoders and scalars


with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)
    
with open('onehot_encoder_location.pkl','rb') as file:
    onehot_encoder_location = pickle.load(file)
    
with open('scalar.pkl','rb') as file: 
    scalar = pickle.load(file)
    
    
    
#streamlit app

st.title('Estimated Salary Pridiction')
location = st.selectbox('Location', onehot_encoder_location.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score= st.number_input('Credit Score')
exited = st.selectbox('Exited',[0, 1])
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number Of Products',1,4)
has_credit_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member',[0, 1])


input_data = pd.DataFrame({
    'CreditScore' : [credit_score],
    'Gender' : [label_encoder_gender.transform([gender])[0]],
    'Age' : [age],
    'Tenure' : [tenure],
    'Balance' : [balance],
    'NumOfProducts' : [num_of_products],
    'HasCreditCard' : [has_credit_card],
    'IsActiveMember' : [is_active_member],
    'Exited' : [exited]
})

#one hot encode 

location_encoded = onehot_encoder_location.transform([[location]]).toarray()
location_encoded_df = pd.DataFrame(location_encoded, columns = onehot_encoder_location.get_feature_names_out(['Location']))

#combine

input_data = pd.concat([input_data.reset_index(drop=True), location_encoded_df], axis=1)


#Scale 

input_data_scaled = scalar.transform(input_data)

#predict churn 
prediction = model.predict(input_data_scaled)
prediction_salary = prediction[0][0]


st.write(f'Predicted Estimated Salary : {prediction_salary:.2f}')
