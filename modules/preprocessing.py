import pandas as pd

def preprocess(df):
    df = df.copy()
    
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Parse date
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df.dropna(subset=['Order Date', 'Quantity', 'Unit Price'], inplace=True)
    
    # Remove invalid values
    df = df[(df['Quantity'] > 0) & (df['Unit Price'] > 0)]
    
    df.reset_index(drop=True, inplace=True)
    return df