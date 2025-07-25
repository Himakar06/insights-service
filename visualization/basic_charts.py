import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px

def plot_histogram(df, column):
    fig = px.histogram(df, x=column, title=f"Histogram of {column}")
    st.plotly_chart(fig, use_container_width=True)

def plot_box(df, column):
    fig = px.box(df, y=column, title=f"Boxplot of {column}")
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(df, column):
    count_data = df[column].value_counts().reset_index()
    count_data.columns = [column, "Count"]
    fig = px.bar(count_data, x=column, y="Count", title=f"Bar Chart of {column}")
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_matrix(df):
    st.subheader("🔗 Correlation Matrix (Numeric Columns)")
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:
        st.info("Not enough numeric columns for correlation matrix.")
        return

    corr = numeric_df.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    st.pyplot(plt)

def plot_scatter(df, col_x, col_y):
    fig = px.scatter(df, x=col_x, y=col_y, title=f"Scatter Plot: {col_x} vs {col_y}")
    st.plotly_chart(fig, use_container_width=True)

def plot_pie(df, column):
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'Count']
    fig = px.pie(value_counts, names=column, values='Count', title=f'Pie Chart of {column}')
    st.plotly_chart(fig, use_container_width=True)

def plot_count(df, column):
    fig = px.histogram(df, x=column, title=f'Count Plot of {column}')
    st.plotly_chart(fig, use_container_width=True)

def plot_line(df , column):
    fig = px.line(df, y=column, title=f'Line Plot of {column}')
    st.plotly_chart(fig, use_container_width=True)