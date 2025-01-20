import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

@st.cache_resource
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        saved_objects = pickle.load(file)
    return saved_objects

# Load the saved XGBoost model
saved_objects = load_model()
xgb_model = saved_objects['xgb_model']

# Load the label encoders from label_encoders.pkl
@st.cache_resource
def load_label_encoders():
    with open('label_encoders.pkl', 'rb') as file:
        return pickle.load(file)

label_encoders = load_label_encoders()

# Define the disease encoder (ensure it includes the correct disease labels from training)
disease_labels = ['anthrax', 'blackleg', 'foot and mouth', 'lumpy virus', 'pneumonia']  # Replace with actual labels
disease_encoder = LabelEncoder()
disease_encoder.fit(disease_labels)

def transform_input(input_data, encoders):
    transformed_data = input_data.copy()

    for column, encoder in encoders.items():
        if column in transformed_data:
            transformed_data[column] = transformed_data[column].apply(
                lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
            )

    return transformed_data

def show_predict_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    .scale-down {
        transform: scale(0.9); /* Adjust the scale factor as needed */
        transform-origin: top left;
    }
    .title {
        font-family: 'Montserrat', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #DADADA;
        text-align: center;
        animation: fadeIn 1.5s ease-in-out;
        letter-spacing: 1px;
        margin-bottom: 10px;
        white-space: nowrap;
    }
    .subtitle {
        font-size: 24px;
        color: #DBAE58;
        text-align: left;
        margin-bottom: 10px;
    }
    .large-font {
        font-size: 18px;
        margin-bottom: 5px;
    }
    .stSelectbox, .stSlider, .stTextInput {
        margin-top: -25px;
    }
    .stSlider > div > div > div > div {
        background: #E0E0E0;
        height: 6px;
        border-radius: 5px;
    }
    .stSlider > div > div > div > div > div {
        background-color: #F1F1F1;
        height: 30px;
        width: 30px;
        border-radius: 50%;
        margin-top: -12px;
        border: 2px solid #488A99;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #488A99;
        font-weight: bold;
    }
    .centered {
        display: flex;
        justify-content: center;
    }
    .animated-text {
        font-size: 36px;
        font-weight: bold;
        animation: colorChange 4s infinite alternate;
    }
    @keyframes colorChange {
        0% { color: #d32d41; }
        50% { color: #ea6a47; }
        100% { color: #0091d5; }
    }
    .prediction-box {
        font-family: 'Montserrat', sans-serif;
        font-size: 20px;
        color: #FFFFFF;
        background-color: #004225;
        border: 2px solid #93B1B5;
        border-radius: 10px;
        padding: 15px;
        margin-top: 5px;
        text-align: center;
    }
    .age-container {
        margin-top: -20px; /* Adjust this value to reduce space above */
        margin-bottom: -5px; /* Adjust this value to reduce space below */
    }
    .age-container span {
        margin-bottom: 0px;
    }
    div[data-testid="stNumberInput"] {
        margin-top: -20px; /* Adjust this value to reduce space between label and input */
    }
    </style>
    <div class="scale-down">
        <div class="title">Livestock Care ⛑️</div>
        <div class="subtitle">*Please provide the following information to predict the disease.</div>
    """, unsafe_allow_html=True)

    # Animal options from the label encoder
    animals = label_encoders['Animal'].classes_

    # Updated symptom options
    symptoms = [
        'fever', 'chills', 'fatigue', 'sores on hooves', 'weight loss', 'coughing',
        'diarrhea', 'blisters', 'swelling', 'nasal discharge', 'blisters on gums',
        'blisters on hooves', 'blisters on mouth', 'blisters on tongue',
        'chest discomfort', 'crackling sound', 'depression', 'difficulty walking',
        'lameness', 'loss of appetite', 'painless lumps', 'shortness of breath',
        'sores on gums', 'sores on mouth', 'sores on tongue', 'sweats',
        'swelling in abdomen', 'swelling in extremities', 'swelling in limb',
        'swelling in muscle', 'swelling in neck'
    ]

    st.markdown('<div class="large-font">Animal</div>', unsafe_allow_html=True)
    animal = st.selectbox("", animals, key="animal_selectbox")

    st.markdown('<div class="large-font">Symptom 1</div>', unsafe_allow_html=True)
    symptom_1 = st.selectbox("", symptoms, key="symptom1_selectbox")

    st.markdown('<div class="large-font">Symptom 2</div>', unsafe_allow_html=True)
    symptom_2 = st.selectbox("", symptoms, key="symptom2_selectbox")

    st.markdown('<div class="large-font">Symptom 3</div>', unsafe_allow_html=True)
    symptom_3 = st.selectbox("", symptoms, key="symptom3_selectbox")

    st.markdown("""
    <style>
    div[data-testid="stNumberInput"] button {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="age-container">
        <span class="large-font">Age (in years)</span>
    </div>
    """, unsafe_allow_html=True)

    age = st.number_input("", min_value=0, max_value=20, value=0, step=1, key="age_number_input")

    st.markdown('<div class="large-font">Temperature</div>', unsafe_allow_html=True)
    temperature = st.text_input("", "103.0", key="temperature_input")

    # Center the predict button
    st.markdown("""
    <style>
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stButton>button {
        margin-top: -10px;
        background-color: #004225;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ffff00;
    }
    .stButton>button:active {
        background-color: #388E3C;
    }
    </style>
    """, unsafe_allow_html=True)

    ok = st.button("Predict Disease")
    
    if ok:
        # Prepare the input for prediction
        sample_data = pd.DataFrame([{
            'Animal': animal,
            'Age': age,
            'Temperature': temperature,
            'Symptom 1': symptom_1,
            'Symptom 2': symptom_2,
            'Symptom 3': symptom_3
        }])

        # Transform the input data using the updated transform_input function
        encoded_input = transform_input(sample_data, label_encoders).values

        # Reshape the input to fit the model
        encoded_input = np.array(encoded_input).reshape(1, -1)

        # Predict with XGBoost and display only the disease
        xgb_prediction = xgb_model.predict(encoded_input)
        xgb_disease = disease_encoder.inverse_transform(xgb_prediction)
        
        # Display the prediction with custom colors and animation
        st.markdown(f"""
        <div class="prediction-box">
            <strong>Predicted Disease:</strong> {xgb_disease[0]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Close the scale-down div