import pandas as pd 

def is_valid_csv(file) -> (bool, str, pd.DataFrame | None):
    try:
        df = pd.read_csv(file)

        if df.empty :
             return False, "CSV file is empty", None

        if df.shape[0] == 0 or df.shape[1] == 0:
            return False, "The file has no valid data", None
        
        return True, "File is valid", df
    
    except Exception as e:
        return False, f"Invalid CSV file: {str(e)}", None
