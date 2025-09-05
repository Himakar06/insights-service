import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from typing import List

@st.cache_data(ttl=3600, show_spinner="Generating quick insights...")
def quick_insights(df: pd.DataFrame, eda_options: List[str]):
    insights = {}

    if "Shape of Dataset" in eda_options:
        insights["Shape of Dataset"] = df.shape

    if "Sample Data" in eda_options:
        insights["Sample Data"] = df.sample(5)

    if "Info" in eda_options:
        buf = io.StringIO()
        df.info(buf=buf)
        insights["Info"] = buf.getvalue()

    if "Describe" in eda_options:
        insights["Describe"] = df.describe()

    if "Null Values Count" in eda_options:
        insights["Null Values Count"] = df.isnull().sum()

    if "Numerical Columns" in eda_options:
        insights["Numerical Columns"] = df.select_dtypes(include=['number']).columns.tolist()

    if "Categorical Columns" in eda_options:
        insights["Categorical Columns"] = df.select_dtypes(include=['object', 'category']).columns.tolist()

    return insights


def generate_null_heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis", ax=ax)
    ax.set_title("Null Values Heatmap")
    return fig


def display_insights():
    st.header("🔎 Manual EDA Explorer")

    if 'df' not in st.session_state:
        st.warning("Please upload a dataset!")
        return
    
    df = st.session_state['df']

    if "eda_results" not in st.session_state:
        st.session_state.eda_results = None
        st.session_state.eda_options = []

    
    eda_options = st.multiselect(
        "Select EDA operations:",
        ["Shape of Dataset", "Sample Data", "Info", "Describe", 
         "Null Values Count", "Numerical Columns", "Categorical Columns"],
        default=st.session_state.eda_options,  
        key="eda_ops"
    )


    if st.button("Show Results", type="primary"):
        if not eda_options:
            st.warning("Please select at least one EDA operation!")
        else:
            st.session_state.eda_options = eda_options
            st.session_state.eda_results = quick_insights(df, eda_options)

   
    if st.session_state.eda_results:
        for option in st.session_state.eda_options:
            st.write(f"### 🔹 {option}")
            result = st.session_state.eda_results[option]

            if option == "Shape of Dataset":
                st.write(result)
            elif option == "Sample Data":
                st.dataframe(result)
            elif option == "Info":
                st.text(result)
            elif option == "Describe":
                st.write(result)
            elif option == "Null Values Count":
                st.write(result)
                if st.checkbox("Show Null Values Heatmap", key="nullmap"):
                    fig = generate_null_heatmap(df)
                    st.pyplot(fig)
            elif option == "numerical_columns":
                st.write("### 🔹 Numerical Columns")
                st.write(result)

            elif option == "categorical_columns":
                st.write("### 🔹 Categorical Columns")
                st.write(result)
            else:
                st.write(result)
