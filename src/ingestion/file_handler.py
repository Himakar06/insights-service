import pandas as pd

def is_valid_csv(file):
    """Check if uploaded file is a valid CSV based on extension."""
    return file.name.endswith('.csv')

def read_csv(file):
    """Reads a CSV file and returns DataFrame or error message."""
    try:
        df = pd.read_csv(file)
        return df, None
    except Exception as e:
        return None, str(e)
