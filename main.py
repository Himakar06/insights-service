import streamlit as st
import pandas as pd
import time

from file_handler import is_valid_csv
from analysis.eda_manual import manual_eda

st.set_page_config(page_title="Insights Service", layout="centered")

st.title("📊 Insights Service")
st.write("Upload a CSV file and start exploring.")

#Reset uploaded file
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "df"  not in st.session_state:
    st.session_state.df= None

# --- File uploader ---
uploaded_file = st.file_uploader(
    "📂 Choose a CSV file",
    type=["csv"],
    accept_multiple_files=False,
    key="file_upload"
)

if uploaded_file is not None and uploaded_file != st.session_state.uploaded_file:
    st.session_state.uploaded_file = uploaded_file

    #progres bar
    progress_text = "⏳ Uploading and processing your file..."
    progress_bar = st.progress(0, text=progress_text)

    for perc in range(0, 101, 20):
        time.sleep(0.2)
        progress_bar.progress(perc, text=progress_text)

    progress_bar.empty()
    
    st.toast("✅ File uploaded successfully!", icon="🎉")

    status, message, df = is_valid_csv(uploaded_file)

    if status and df is not None:
        st.session_state.df = df
        
        st.info(f"**Filename:** {uploaded_file.name}")
        st.write("**Shape:**", df.shape)

        st.write("**Data Preview**")
        st.dataframe(df.head())
    
    else:
        st.session_state.df = None
        st.error(f"❌ {message}")
      
#EDA Manual
st.title("📊 Manual EDA")
if st.session_state.df is not None:
    manual_eda(st.session_state.df)

