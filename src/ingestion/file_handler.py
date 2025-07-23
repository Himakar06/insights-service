import pandas as pd

MAX_FILE_SIZE_MB = 5  # Max upload size limit


def is_valid_csv(file):
    """Check if uploaded file is a valid CSV based on extension."""
    return file.name.endswith('.csv')


def is_file_size_valid(file):
    """Check if file size is within the limit."""
    return file.size <= MAX_FILE_SIZE_MB * 1024 * 1024


def read_csv(file):
    """Attempts to read a CSV file using different encodings if utf-8 fails."""
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(file, encoding=encoding)
            return df, None
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return None, f"Unexpected error while reading CSV: {e}"
    
    return None, "Failed to read the file with common encodings (utf-8, ISO-8859-1, cp1252)."


def handle_missing_values(df: pd.DataFrame, important_cols: list = None, drop_threshold: float = 0.5):
    """
    Handles missing values:
    - Drops columns with nulls > threshold (if not important)
    - Fills numeric columns with mean/median based on skewness
    """
    important_cols = important_cols or []
    total_rows = df.shape[0]
    updated_df = df.copy()
    dropped_cols = []
    filled_cols = {}

    for col in df.columns:
        null_ratio = df[col].isnull().sum() / total_rows

        if null_ratio > drop_threshold and col not in important_cols:
            updated_df.drop(columns=[col], inplace=True)
            dropped_cols.append(col)
        elif df[col].isnull().sum() > 0:
            if df[col].dtype in ['float64', 'int64']:
                skew = df[col].skew()
                if abs(skew) > 1:
                    fill_value = df[col].median()
                    strategy = 'median'
                else:
                    fill_value = df[col].mean()
                    strategy = 'mean'
                updated_df[col].fillna(fill_value, inplace=True)
                filled_cols[col] = strategy

    return updated_df, dropped_cols, filled_cols


def validate_dataframe(df):
    """Checks for missing values and column type issues, then handles them."""
    issues = {}

    if df.empty:
        issues['empty_file'] = "The uploaded CSV file is empty."

    if df.isnull().sum().sum() > 0:
        issues['missing_values'] = "The file contains missing values."

    num_cols = df.select_dtypes(include=['number']).shape[1]
    obj_cols = df.select_dtypes(include=['object']).shape[1]

    if num_cols == 0:
        issues['numeric_columns'] = "No numeric columns detected."
    if obj_cols == 0:
        issues['text_columns'] = "No text/object columns detected."

    # Proceed to handle missing values only if not empty
    df_cleaned, dropped_cols, filled_cols = handle_missing_values(df)

    return issues, df_cleaned, dropped_cols, filled_cols
