import pandas as pd

def generate_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generates basic statistics summary of the dataset."""
    summary = pd.DataFrame()

    numeric_cols = df.select_dtypes(include=['number']).columns

    summary['Mean'] = df[numeric_cols].mean()
    summary['Median'] = df[numeric_cols].median()
    summary['Null Count'] = df[numeric_cols].isnull().sum()
    summary['Unique Count'] = df[numeric_cols].nunique()
    summary['Skewness'] = df[numeric_cols].skew()

    return summary.round(2)
