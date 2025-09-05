import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data(ttl=3600, show_spinner="Calculating data quality score...")
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
    dtypes_score = 20 * (1- (abs( numeric_cols - categoric_cols) / max(1, df.shape[1])))
    total_score += dtypes_score
    factors.append(f"Data Types: {dtypes_score:.1f}/20 ({numeric_cols} numeric, {categoric_cols} categorical)")

    #4.Column Names (10points)
    invalid_chars = sum(1 for col in df.columns if any(c in col for c in [' ', '-', '*', '/', '.']))
    naming_score = 10 * (1 - (invalid_chars / max(1, len(df.columns))))
    total_score += naming_score
    factors.append(f"Column Names: {naming_score:.1f}/10 ({invalid_chars} columns with special chars)")

    #5.Data Volume (15points)
    volume_score = min(15, (df.shape[0] * df.shape[1])/1000)
    total_score += volume_score
    factors.append(f"Data Volume: {volume_score:.1f}/15 ({df.shape[0]} rows × {df.shape[1]} columns)")

    #6.Outliers (15points)
    numeric_cols_count = df.select_dtypes(include=[np.number]).shape[1]
    if numeric_cols_count > 0:
        outlier_scores = []
        numeric_df = df.select_dtypes(include=[np.number])
        for col in numeric_df.columns:
            if numeric_df[col].notna().sum() > 0:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                if IQR > 0:
                    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                    outlier_percentage = outliers / df.shape[0]
                    outlier_scores.append(1 - outlier_percentage)
                else:
                    outlier_scores.append(1.0)
        if outlier_scores:
            outlier_score = 15 * (sum(outlier_scores) / len(outlier_scores))
            total_score += outlier_score
            factors.append(f"Outliers: {outlier_score:.1f}/15 (numeric columns analysis)")
        else:
            factors.append("Outliers: N/A (no valid numeric columns for analysis)")
    else:
        factors.append("Outliers: N/A (no numeric columns)")

    total_score = max(0 , min(100, total_score))

    return total_score, factors

@st.cache_data(ttl=3600)
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
        if "Missing values" in factors[0] and float(factors[0].split(":")[1].split("/")[0].strip()) < 20:
            st.write("• Consider handling missing values (imputation or removal)")
        
        if "Duplicates" in factors[1] and float(factors[1].split(":")[1].split("/")[0].strip()) < 12:
            st.write("• Remove duplicate rows")
        
        if "Data Types" in factors[2] and float(factors[2].split(":")[1].split("/")[0].strip()) < 15:
            st.write("• Validate and convert data types appropriately")
        
        if "Column Names" in factors[3] and float(factors[3].split(":")[1].split("/")[0].strip()) < 8:
            st.write("• Standardize column names (remove special characters)")
        
        if "Outliers" in factors[-1] and "N/A" not in factors[-1]:
            outlier_score = float(factors[-1].split(":")[1].split("/")[0].strip())
            if outlier_score < 12:
                st.write("• Investigate and handle outliers in numeric columns")