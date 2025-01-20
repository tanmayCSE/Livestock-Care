import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

@st.cache_resource
def load_data():
    # Example livestock dataset with specified animals and all symptoms
    data = {
        "Animal": ["Cow", "Buffalo", "Sheep", "Goat", "Cow", "Sheep", "Goat"],
        "Age": [5, 3, 2, 3, 4, 6, 4],
        "Temperature": [101.5, 102.0, 103.0, 102.2, 101.8, 104.1, 100.9],
        "Symptom 1": ["Fever", "Chills", "Fatigue", "Sores on hooves", "Weight loss", "Coughing", "Diarrhea"],
        "Symptom 2": ["Blisters", "Swelling", "Nasal discharge", "Blisters on gums", "Blisters on hooves", "Blisters on mouth", "Blisters on tongue"],
        "Symptom 3": ["Chest discomfort", "Crackling sound", "Depression", "Difficulty walking", "Lameness", "Loss of appetite", "Painless lumps"],
        "Disease": ["Lumpy Virus", "Foot and Mouth", "Anthrax", "Blackleg", "Pneumonia", "Foot and Mouth", "Lumpy Virus"]
    }

    df = pd.DataFrame(data)
    return df

def show_explore_page():
    st.title("Explore Livestock Disease Dataset")

    st.write(
        """
    ### Livestock Disease Prediction Data Exploration
    """
    )

    df = load_data()

    # Distribution of Animals
    st.write("#### Distribution of Animals")
    animal_counts = df["Animal"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(animal_counts, labels=animal_counts.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.pyplot(fig1)

    # Mean Temperature by Animal
    st.write("#### Mean Temperature by Animal")
    temp_by_animal = df.groupby("Animal")["Temperature"].mean()
    st.bar_chart(temp_by_animal)

    # Mean Age by Disease
    st.write("#### Mean Age by Disease")
    age_by_disease = df.groupby("Disease")["Age"].mean()
    st.bar_chart(age_by_disease)

    # Count of Symptoms with Different Colors
    st.write("#### All Symptoms")
    symptom_data = pd.concat([
        df["Symptom 1"],
        df["Symptom 2"],
        df["Symptom 3"]
    ])

    symptom_counts = symptom_data.value_counts()

    # Define colors for each symptom
    colors = plt.cm.tab20.colors[:len(symptom_counts)]

    fig2, ax2 = plt.subplots()
    ax2.bar(symptom_counts.index, symptom_counts.values, color=colors)
    ax2.set_xticklabels(symptom_counts.index, rotation=90)
    ax2.set_ylabel("Count")
    ax2.set_title("Symptom Counts")

    st.pyplot(fig2)

    # Creative Feature: Age Distribution with Interactive Slider
    st.write("#### Age Distribution")
    age_slider = st.slider("Select Age Range", min_value=int(df["Age"].min()), max_value=int(df["Age"].max()), value=(int(df["Age"].min()), int(df["Age"].max())))
    filtered_df = df[(df["Age"] >= age_slider[0]) & (df["Age"] <= age_slider[1])]
    st.bar_chart(filtered_df["Age"].value_counts().sort_index())

# Main entry point
if __name__ == "__main__":
    show_explore_page()