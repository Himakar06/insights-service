import streamlit as st
import pandas as pd
import os
import sys

# Add root path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import custom handlers
from src.ingestion.file_handler import read_csv, is_valid_csv, is_file_size_valid, validate_dataframe
from src.analysis.summary import generate_summary
from src.analysis.autoeda import generate_eda_report
from src.visualization.basic_charts import (
    plot_histogram,
    plot_box,
    plot_bar,
    plot_pie,
    plot_count,
    plot_scatter,
    plot_line,
    plot_correlation_matrix
)

# Streamlit page config
st.set_page_config(page_title='CSV Upload & Validation', layout='centered')
st.title("📁 Upload and Validate Your CSV File")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV File", type=['csv'])

if uploaded_file is not None:
    # Show file details
    file_details = {
        "File name": uploaded_file.name,
        "File type": uploaded_file.type,
        "Size (KB)": round(uploaded_file.size / 1024, 2)
    }
    st.success("✅ File uploaded successfully!")
    st.json(file_details)

    # Validate file extension and size
    if not is_valid_csv(uploaded_file):
        st.error("❌ Invalid file format. Please upload a .csv file.")
    elif not is_file_size_valid(uploaded_file):
        st.error("❌ File size exceeds the 5 MB limit.")
    else:
        with st.spinner("Processing and validating your file..."):
            # Read CSV
            df, error = read_csv(uploaded_file)

            if error:
                st.error(f"❌ Error reading the file: {error}")
            else:
                # Run validation and cleaning
                issues, df_cleaned, dropped_cols, filled_cols = validate_dataframe(df)

                if issues:
                    st.warning("⚠️ Data validation issues found:")
                    for key, msg in issues.items():
                        st.warning(f"- {msg}")
                else:
                    st.success("✅ File validated successfully!")

                # Show results of missing value handling
                if dropped_cols:
                    st.warning(f"🚫 Dropped columns due to too many nulls: {', '.join(dropped_cols)}")

                if filled_cols:
                    st.success("🧩 Filled missing values using:")
                    for col, method in filled_cols.items():
                        st.info(f"{col}: filled with {method}")

                # Show cleaned data preview
                st.write(f"🧮 Rows: {df_cleaned.shape[0]}, Columns: {df_cleaned.shape[1]}")
                st.subheader("📊 Cleaned Data Preview")
                st.dataframe(df_cleaned.head())

                # Show updated summary
                st.subheader("📈 Summary After Cleaning")
                summary_df = generate_summary(df_cleaned)
                st.dataframe(summary_df)
                
                st.subheader("📊 Generate AutoEDA Report with Sweetviz")
                if st.button("Run AutoEDA"):
                    with st.spinner("Generating EDA report..."):
                        output_path = generate_eda_report(df)

                        if os.path.exists(output_path):
                            st.success("✅ Report generated successfully!")

                            with open(output_path, "rb") as f:
                                st.download_button(
                                    label="📥 Download EDA Report",
                                    data=f,
                                    file_name="sweetviz_report.html",
                                    mime="text/html"
                                )
                        else:
                            st.error("❌ Failed to generate EDA report.")

                st.subheader("📊 Custom Column-wise Visualizations")

                columns = ['None'] + df.columns.tolist()
                chart_types = ['None','Bar','Line','Pie','Box','Histogram','Count','Scatter']

                col1 , col2 = st.columns(2)
                selected_column = col1.selectbox("Choose a column",columns)
                selected_chart = col2.selectbox("Choose a chart",chart_types)

                if selected_column != 'None' and selected_chart != 'None':
                    if selected_column in df.columns:
                        try:
                            if selected_chart == 'Bar':
                                plot_bar(df, selected_column)
                            elif selected_chart == 'Pie':
                                plot_pie(df, selected_column)
                            elif selected_chart == 'Box':
                                plot_box(df, selected_column)
                            elif selected_chart == 'Count':
                                plot_count(df, selected_column)
                            elif selected_chart == 'Histogram':
                                plot_hist(df, selected_column)
                            elif selected_chart == 'Line':
                                plot_line(df, selected_column)
                            elif selected_chart == 'Scatter':
                                plot_scatter(df, selected_column)
                        except Exception as e:
                            st.error(f"❌ Failed to generate {selected_chart} for '{selected_column}': {e}")
                    else:
                        st.warning(f"⚠️ Column '{selected_column}' not found in dataset.")
                else:
                    st.info("Select both a column and a chart type to display the visualization.")

else:
    st.info("📥 Please upload a CSV file to get started.")
