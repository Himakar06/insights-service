import pandas as pd
import numpy as np
import streamlit as st

def calculate_score(df):
    total_score = 0
    max_score = 100
    factors = []

    #1.Missing values (25points)
    missing_percentage = df.isnull().sum().sum()/ (df.shape[0] * df.shape[1])
    missing_score = 25 * (1 - missing_percentage)
    total_score += missing_score
    factors.append(f"Missing values: {missing_score:.1f}/25 ({missing_percentage:.1%} missing)")

    #2.Duplicates (15points)
    duplicate_percentage = df.duplicated().sum()/ df.shape[0]
    duplicate_score = 15*(1 - duplicate_percentage)
    total_score += duplicate_score
    factors.append(f"Duplicates: {duplicate_score:.1f}/15 ({duplicate_percentage:.1%} duplicates)")

    #3.Data types consistency (20points)
    numeric_cols = df.select_dtypes(include=[np.number]).shape[1]
    categoric_cols = df.select_dtypes(include=['object', 'category']).shape[1]
    dtypes_score = 20 * (1- (abs( numeric_cols - categoric_cols) / df.shape[1]))
    total_score += dtypes_score
    factors.append(f"Data Types: {dtypes_score:.1f}/20 ({numeric_cols} numeric, {categoric_cols} categorical)")

    #4.Column Names (10points)
    invalid_chars = sum(1 for col in df.columns if any(c in col for c in [' ', '-', '*', '/', '.']))
    naming_score = 10 * (1 - (invalid_chars / len(df.columns)))
    total_score += naming_score
    factors.append(f"Column Names: {naming_score:.1f}/10 ({invalid_chars} columns with special chars)")

    #5.Data Volume (15points)
    volume_score = min(15, (df.shape[0] * df.shape[1])/1000)
    total_score += volume_score
    factors.append(f"Data Volume: {volume_score:.1f}/15 ({df.shape[0]} rows × {df.shape[1]} columns)")

    #6.Outliers (15points)
    if numeric_cols > 0:
        outlier_scores = []
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            outlier_percentage = outliers / df.shape[0]
            outlier_scores.append(1 - outlier_percentage)

        outlier_score = 15 * (sum(outlier_scores) / len(outlier_scores))
        total_score += outlier_score
        factors.append(f"Outliers: {outlier_score:.1f}/15 (numeric columns analysis)")

    else:
        factors.append("Outliers: N/A (no numeric columns)")

    total_score = max(0 , min(100, total_score))

    return total_score, factors


def get_quality_emoji(score):
    if score >= 90:
        return "🎯 Excellent"
    elif score >= 75:
        return "👍 Good"
    elif score >= 60:
        return "⚠️ Fair"
    elif score >= 40:
        return "🔧 Needs Improvement"
    else:
        return "❌ Poor"
    
def display_quality_score(score, factors):
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📊 Data Quality Score")
        
        # Create a progress bar-like display
        progress_color = "green" if score >= 75 else "orange" if score >= 50 else "red"
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {progress_color} {score}%, #f0f0f0 {score}%);
                   height: 30px; border-radius: 15px; display: flex; align-items: center;
                   justify-content: center; font-weight: bold; color: {'white' if score > 50 else 'black'};
                   margin: 10px 0;">
            {score:.1f}/100 - {get_quality_emoji(score)}
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📋 Quality Factors Breakdown"):
        for factor in factors :
            st.write(f"• {factor}")

    if score < 75:
        st.warning("💡 **Recommendations:**")
        if score < 60:
            st.write("• Consider handling missing values")
            st.write("• Remove duplicate rows")
            st.write("• Check for data entry errors")
        st.write("• Review column names for consistency")
        st.write("• Validate data types")