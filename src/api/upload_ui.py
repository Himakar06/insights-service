import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from src.ingestion.file_handler import read_csv, is_valid_csv


import streamlit as st 
import pandas as pd

from src.ingestion.file_handler import read_csv, is_valid_csv

st.set_page_config(page_title='CSV UPLOAD', layout='centered')
st.title("📁 Upload Your CSV File")

uploaded_file = st.file_uploader("Choose a CSV File", type=['csv'])

if uploaded_file is not None:
    file_details={
        "File name" : uploaded_file.name,
        "File type" : uploaded_file.type,
        "Size (KB)" : round(uploaded_file.size/1024 , 2)
    }
    
    st.success("✅ File uploaded successfully!")
    st.json(file_details)

    with st.spinner("Processing..."):
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Upload and read complete ✅")
            st.write(f"🧮 Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            st.subheader("📊 Preview of Data")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Error reading the file: {e}")
else:
    st.info("Please upload a CSV file to continue.")