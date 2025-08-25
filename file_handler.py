import pandas as pd

def is_valid_csv(file) -> (bool, str, pd.DataFrame | None):
    try:
    
        df = pd.read_csv(file, encoding="utf-8", low_memory=False)

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
