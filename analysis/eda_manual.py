import io
import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

def manual_eda(df: pd.DataFrame):
    st.header("🔎 Manual EDA Explorer")

    eda_options = st.multiselect(
        "Select EDA operations:",
        ["Shape of Dataset", "Sample Data", "Info", "Describe", 
         "Null Values Count", "Numerical Columns", "Categorical Columns"]
    )

    if st.button("Show Results"):
        if "Shape of Dataset" in eda_options:
            st.write("### 🔹 Shape")
            st.dataframe(df.head())

        if "Sample Data" in eda_options:
            st.write("### 🔹 Sample Data()")
            st.dataframe(df.sample(5)) 

        if "Info" in eda_options:
            st.write("### 🔹 DataFrame Info")
            buf = io.StringIO()
            df.info(buf=buf)
            st.text(buf.getvalue())

        if "Describe" in eda_options:
            st.write("### 🔹 Describe()")
            st.write(df.describe())

        if "Null Values Count" in eda_options:
            st.write("### 🔹 Missing Values")
            st.write(df.isnull().sum())

        if "Numerical Columns" in eda_options:
            st.write("### 🔹 Numerical Columns")
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            st.write(num_cols)

        if "Categorical Columns" in eda_options:
            st.write("### 🔹 Categorical Columns")
            cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
            st.write(cat_cols)