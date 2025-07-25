import streamlit as st
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

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
from src.export.pdf_exporter import PDFReport

# Streamlit page config
st.set_page_config(page_title='CSV Upload & Validation', layout='centered')

st.title("📁 Upload and Validate Your CSV File")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV File", type=['csv'])

if uploaded_file is not None:
    if "chart_blocks" not in st.session_state:
        st.session_state.chart_blocks = [0]
        st.session_state.next_block_id = 1

    if "chart_config" not in st.session_state:
        st.session_state.chart_config = {}

    file_details = {
        "File name": uploaded_file.name,
        "File type": uploaded_file.type,
        "Size (KB)": round(uploaded_file.size / 1024, 2)
    }
    st.success("✅ File uploaded successfully!")
    st.json(file_details)

    if not is_valid_csv(uploaded_file):
        st.error("❌ Invalid file format. Please upload a .csv file.")
    elif not is_file_size_valid(uploaded_file):
        st.error("❌ File size exceeds the 5 MB limit.")
    else:
        with st.spinner("Processing and validating your file..."):
            df, error = read_csv(uploaded_file)

            if error:
                st.error(f"❌ Error reading the file: {error}")
            else:
                issues, df_cleaned, dropped_cols, filled_cols = validate_dataframe(df)

                if issues:
                    st.warning("⚠️ Data validation issues found:")
                    for key, msg in issues.items():
                        st.warning(f"- {msg}")
                else:
                    st.success("✅ File validated successfully!")

                if dropped_cols:
                    st.warning(f"🚫 Dropped columns due to too many nulls: {', '.join(dropped_cols)}")

                if filled_cols:
                    st.success("🧩 Filled missing values using:")
                    for col, method in filled_cols.items():
                        st.info(f"{col}: filled with {method}")

                st.write(f"🧮 Rows: {df_cleaned.shape[0]}, Columns: {df_cleaned.shape[1]}")
                st.subheader("📊 Cleaned Data Preview")
                st.dataframe(df_cleaned.head())

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

                def render_chart_block(block_id):
                    col1, col2, col3 = st.columns([4, 4, 1])
                    column_options = ['None'] + df.columns.tolist()
                    chart_options = ['None', 'Bar', 'Line', 'Pie', 'Box', 'Histogram', 'Count', 'Scatter']

                    selected_column = col1.selectbox(f"🔸 Select Column #{block_id}", column_options, key=f"col_{block_id}")
                    selected_chart = col2.selectbox(f"🔹 Select Chart Type #{block_id}", chart_options, key=f"chart_{block_id}")

                    if col3.button("❌", key=f"remove_{block_id}"):
                        st.session_state.chart_blocks.remove(block_id)
                        st.session_state.chart_config.pop(block_id, None)
                        st.rerun()

                    if selected_column != "None" and selected_chart != "None":
                        st.session_state.chart_config[block_id] = (selected_chart, selected_column)
                        st.markdown(f"### 📊 {selected_chart} of `{selected_column}`")
                        try:
                            fig, ax = plt.subplots(figsize=(8, 4))
                            image_path = f"temp_chart_{block_id}_{selected_chart}_{selected_column}.png"

                            if selected_chart == 'Bar':
                                df[selected_column].value_counts().plot(kind='bar', ax=ax)
                            elif selected_chart == 'Pie':
                                df[selected_column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
                            elif selected_chart == 'Box':
                                df[selected_column].plot(kind='box', ax=ax)
                            elif selected_chart == 'Count':
                                df[selected_column].value_counts().plot(kind='bar', ax=ax)
                            elif selected_chart == 'Histogram':
                                df[selected_column].plot(kind='hist', bins=20, ax=ax)
                            elif selected_chart == 'Line':
                                df[selected_column].plot(kind='line', ax=ax)
                            elif selected_chart == 'Scatter':
                                ax.scatter(df.index, df[selected_column])

                            ax.set_title(f"{selected_chart} of {selected_column}")
                            plt.tight_layout()
                            plt.savefig(image_path)
                            plt.close(fig)

                            st.session_state.chart_config[block_id] += (image_path,)
                            st.image(image_path)

                        except Exception as e:
                            st.error(f"❌ Failed to render {selected_chart} for {selected_column}: {e}")

                st.markdown("Build your own chart panel by selecting columns and chart types. Click ➕ to add more.")

                for block_id in st.session_state.chart_blocks:
                    render_chart_block(block_id)
                    st.markdown("---")

                if st.button("➕ Add Another Chart"):
                    st.session_state.chart_blocks.append(st.session_state.next_block_id)
                    st.session_state.next_block_id += 1
                    st.rerun()

                st.markdown('---')
                try:
                    plot_correlation_matrix(df)
                except Exception as e:
                    st.error(f"❌ Failed to generate correlation matrix: {e}")

                st.subheader("📄 Export Dashboard as PDF")

                if st.button("🖨️ Generate PDF Report"):
                    try:
                        pdf = PDFReport()
                        pdf.add_page()

                        pdf.add_section_title("Dataset Summary")
                        pdf.add_text(f"Total Rows: {df_cleaned.shape[0]}\nTotal Columns: {df_cleaned.shape[1]}")

                        pdf.add_table(summary_df.head(10), title="Statistical Summary (Top 10 Rows)")

                        corr_img_path = "temp_corr_plot.png"
                        corr = df_cleaned.select_dtypes(include='number').corr()
                        plt.figure(figsize=(10, 6))
                        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
                        plt.tight_layout()
                        plt.savefig(corr_img_path)
                        plt.close()
                        pdf.add_image(corr_img_path, title="Correlation Matrix")

                        for block_id in st.session_state.chart_blocks:
                            if block_id in st.session_state.chart_config:
                                chart_type, column, image_path = st.session_state.chart_config[block_id]
                                pdf.add_image(image_path, title=f"{chart_type} of {column}")

                        output_path = "dashboard_summary.pdf"
                        pdf.output(output_path)

                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=f,
                                file_name="dashboard_summary.pdf",
                                mime="application/pdf"
                            )

                        paths_to_cleanup = [corr_img_path] + [cfg[2] for cfg in st.session_state.chart_config.values() if len(cfg) == 3]
                        for path in paths_to_cleanup:
                            if os.path.exists(path):
                                os.remove(path)

                        st.session_state.chart_config.clear()

                    except Exception as e:
                        st.error(f"❌ Failed to generate PDF: {e}")
else:
    st.info("📥 Please upload a CSV file to get started.")
