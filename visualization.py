import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def initialize_session_state():
    if 'chart_blocks' not in st.session_state:
        st.session_state.chart_blocks = [0]
    if 'next_block_id' not in st.session_state:
        st.session_state.next_block_id = 1
    if 'chart_config' not in st.session_state:
        st.session_state.chart_config = {}

def render_charts(block_id, df):
    col1, col2, col3 = st.columns([4,4,1])
    column_options = ['None'] + df.columns.tolist()
    chart_options = ['None', 'Bar Graph', 'Line Chart','Pie Chart', 'Count Plot', 'Histogram', 'Box Plot', 'Scatter Plot', 'Correlation Heatmap']
    selected_column = col1.selectbox("Select Column #{block_id}", column_options, key=f"col_{block_id}")
    selected_chart = col2.selectbox("Select Chart Type#{block_id}", chart_options, key=f"chart_{block_id}")

    second_column = None
    if selected_chart in ['Scatter Plot', 'Correlation Heatmap']:
        second_column = col1.selectbox("Select Second Column #{block_id}", column_options, key=f"col2_{block_id}")

    if col3.button("❌", key = f"remove_{block_id}"):
        st.session_state.chart_blocks.remove(block_id)
        st.session_state.chart_config.pop(block_id, None)
        st.rerun()

    