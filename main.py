import streamlit as st
import pandas as pd
import time

from file_handler import is_valid_csv
from analysis.quick_insights import quick_insights
from analysis.auto_eda import generate_eda

st.set_page_config(page_title="Insights Service", layout="centered")

st.title("📊 Insights Service")
st.write("Upload a CSV file and start exploring.")

#Reset uploaded file
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "df"  not in st.session_state:
    st.session_state.df= None

if "show_preview" not in st.session_state:
    st.session_state.show_preview = False

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
        st.session_state.show_preview = True
        
    else:
        st.session_state.df = None
        st.session_state.show_preview = False
        st.error(f"❌ {message}")

if st.session_state.df is not None:

        st.info(f"**Filename:** {st.session_state.uploaded_file.name}")
        st.write("**Shape:**", st.session_state.df.shape)

        if st.session_state.show_preview:
            st.write("**Data Preview**")
            st.dataframe(st.session_state.df.head())
    

    #Quick insights
        st.title("📊 Quick Insights")
        quick_insights(st.session_state.df)

    #Auto EDA
        st.subheader("🔎 Auto Generate EDA")    
        st.write(  "This feature uses **ydata_profiling** to create a complete exploratory data analysis (EDA) report.")

        if st.button("Generate Auto EDA"):
            with st.spinner("Generating EDA Report... Please wait ⏳"):
                report_path = "eda_report.html"
                generate_eda(st.session_state.df, report_path)

            st.toast("✅ Auto EDA Report Generated!")

            with open(report_path, "r", encoding= "utf-8") as f:
                html_content = f.read()
                st.components.v1.html(html_content, height=800,  scrolling = True)

            with open(report_path, "rb") as f:
                st.download_button(
                    label = "Download EDA Report",
                    data=f,
                    file_name = "eda_report.hmtl",
                    mime="text/html"
                )