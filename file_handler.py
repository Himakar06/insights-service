import pandas as pd
import hashlib
import streamlit as st

def get_file_hash(file):
    file.seek(0)
    content = file.read()
    file.seek(0)
    return hashlib.md5(content).hexdigest()

@st.cache_data(ttl=3600)
def read_csv_file(file_path_or_object):
    return pd.read_csv(file_path_or_object, encoding="utf-8", low_memory=False)


def is_valid_csv(file) -> (bool, str, pd.DataFrame | None):
    try:
        
        file_hash = get_file_hash(file)

        df = read_csv_file(file)

        if df.empty:
            return False, "CSV file is empty", None

        if df.shape[0] < 1 or df.shape[1] < 1:
            return False, "The file has no valid data", None

        if any(col is None or str(col).strip() == "" for col in df.columns):
            return False, "CSV file has missing/invalid column names", None

        return True, "File is valid", df

    except UnicodeDecodeError:
        return False, "Encoding error: Try saving as UTF-8", None

    except pd.errors.EmptyDataError:
        return False, "CSV file has no data", None

    except pd.errors.ParserError:
        return False, "Parsing error: Check delimiters or corrupted file", None

    except Exception as e:
        return False, f"Invalid CSV file: {str(e)}", None
