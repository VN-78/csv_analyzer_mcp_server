# region Overview
"""
Csv File Reader 

Example usage:
- 'what is in sample.csv'
- 'how many columns are in sample.csv '
- 'how many rows are in sample.csv'
"""
# endregion

#region imports
import pandas as pd
from pathlib import Path
#endregion


# region tools

def read_csv(file_path: str) -> str:
    """
    Reads an Csv file and returns its contents
    Use When analyzing an csv file or reading an csv file 
    Examples : 'Read sample.csv' , 'Whats in sample.csv' , 'what is in the csv file'
    Args:
        file_path: path to the csv file , ask the user if not specified 
        
    Returns:
        str: contents of the csv file and file info and summary
    """
    
    try:
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            return f"File {file_path} does not exist"
        
        df = pd.read_csv(file_path_obj)
        
        result = f"Successfully Read Csv file : {file_path_obj}\n"
        result += f"{df.shape[0]} rows and {df.shape[1]} columns\n"
        result += f"Columns in the file : {', '.join(df.columns)}\n\n"
        result += "First 5 rows:\n"
        result += df.head().to_string()
        
        return result
    
    except Exception as e:
        return f"Error reading file : {str(e)}"
        
#endregion        
