import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def initialize_session_state():
    if 'chart_blocks' not in st.session_state:
        st.session_state.chart_blocks = [0]
    if 'next_block_id' not in st.session_state:
        st.session_state.next_block_id = 1
    if 'chart_config' not in st.session_state:
        st.session_state.chart_config = {}
    if 'saved_charts' not in st.session_state:
        st.session_state.saved_charts = {}

def render_charts(block_id, df):
    col1, col2, col3 = st.columns([4, 4, 1])
    column_options = ['None'] + df.columns.tolist()
    chart_options = ['None', 'Bar Graph', 'Pie Chart', 'Line Chart',
                     'Count Plot', 'Histogram', 'Box Plot',
                     'Scatter Plot', 'Correlation Heatmap']
    
    selected_column = col1.selectbox(f"Select Column #{block_id}", column_options, key=f"col_{block_id}")
    selected_chart = col2.selectbox(f"Select Chart Type #{block_id}", chart_options, key=f"chart_{block_id}")

    second_column = None
    if selected_chart in ['Scatter Plot', 'Correlation Heatmap']:
        second_column = col1.selectbox(f"Select Second Column #{block_id}", column_options, key=f"col2_{block_id}")

    if col3.button("❌", key=f"remove_{block_id}"):
        st.session_state.chart_blocks.remove(block_id)
        st.session_state.chart_config.pop(block_id, None)
        st.session_state.saved_charts.pop(block_id, None)
        st.rerun()

    if selected_column != 'None' and selected_chart != 'None':
        if selected_chart in ['Scatter Plot', 'Correlation Heatmap'] and (second_column == 'None' or second_column is None):
            st.warning("⚠️ Please select a second column for this chart type")
            return

        # save config
        st.session_state.chart_config[block_id] = (selected_chart, selected_column, second_column)

        try:
            fig = None
            if selected_chart == 'Bar Graph':
                value_counts = df[selected_column].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                             title=f"Bar Chart of {selected_column}",
                             labels={'x': selected_column, 'y': 'Count'})
            elif selected_chart == 'Pie Chart':
                fig = px.pie(df, names=selected_column, title=f"Pie Chart of {selected_column}")
            elif selected_chart == 'Line Chart':
                fig = px.line(df, y=selected_column, title=f"Line Chart of {selected_column}")
            elif selected_chart == 'Count Plot':
                value_counts = df[selected_column].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                             title=f"Count Plot of {selected_column}",
                             labels={'x': selected_column, 'y': 'Frequency'})
            elif selected_chart == 'Histogram':
                fig = px.histogram(df, x=selected_column, nbins=20, title=f"Histogram of {selected_column}")
            elif selected_chart == 'Box Plot':
                fig = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
            elif selected_chart == 'Scatter Plot':
                fig = px.scatter(df, x=selected_column, y=second_column,
                                 title=f"Scatter Plot: {selected_column} vs {second_column}")
            elif selected_chart == "Correlation Heatmap":
                if pd.api.types.is_numeric_dtype(df[selected_column]) and pd.api.types.is_numeric_dtype(df[second_column]):
                    correlation = df[selected_column].corr(df[second_column])
                    fig = px.scatter(df, x=selected_column, y=second_column, trendline='ols')
                    fig.add_annotation(
                        x=0.05, y=0.95,
                        xref="paper", yref="paper",
                        text=f"Correlation: {correlation:.3f}",
                        showarrow=False,
                        bgcolor="white",
                        bordercolor="black",
                        borderwidth=1
                    )
                else:
                    st.error("Both columns must be numerical for correlation analysis")
                    return

            if fig:
                fig.update_layout(
                    height=400,
                    showlegend=selected_chart in ['Pie Chart', 'Scatter Plot'],
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.session_state.saved_charts[block_id] = fig
                st.plotly_chart(fig,use_container_width=True, key=f"chart_{block_id}_{selected_chart}_{selected_column}_{second_column or ''}")


        except Exception as e:
            st.error(f"❌ Failed to render {selected_chart} for {selected_column}: {e}")

def visualize_columns(df):
    if df is None or df.empty:
        st.warning("No data available for visualization!")
        return
    
    initialize_session_state()
    st.markdown("Build your own chart panel by selecting columns and chart types. Click ➕ to add more.")

    # only render via render_charts (no duplicate plotting)
    for block_id in st.session_state.chart_blocks:
        render_charts(block_id, df)
        st.markdown('---')

    if st.button("➕ Add Chart"):
        st.session_state.chart_blocks.append(st.session_state.next_block_id)
        st.session_state.next_block_id += 1
        st.rerun()

    st.markdown("---")

def show_full_correlation_matrix(df):
    numerical_df = df.select_dtypes(include=[np.number])
    if len(numerical_df.columns) > 1:
        st.subheader("📊 Complete Correlation Matrix")
        corr_matrix = numerical_df.corr()
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title='Correlation Matrix Heatmap'
        )
        st.plotly_chart(fig, use_container_width=True, key="corr_matrix")
    else:
        st.info("Need at least two numerical columns for correlation matrix.")
