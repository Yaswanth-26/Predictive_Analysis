import pandas as pd
import numpy as np
from scipy.stats import shapiro
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """Load the crime dataset from a CSV file."""
    return pd.read_csv(file_path)

def load_economic_data(file_path):
    """Load the economic factors dataset."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Clean and preprocess the crime dataset."""
    # Handle missing values
    obj_cols = ['Mocodes', 'Vict Sex', 'Vict Descent', 'Premis Desc', 'Weapon Desc']
    drop_cols = ['Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street']
    num_cols = ['Premis Cd', 'Weapon Used Cd', 'Crm Cd 1']
    
    # Drop columns with high percentage of missing values
    df.drop(drop_cols, axis=1, inplace=True)
    
    # Fill object columns with mode
    for col in obj_cols:
        mode_value = df[col].mode()[0]
        df[col].fillna(mode_value, inplace=True)
    
    # Fill numeric columns with mean
    for col in num_cols:
        df[col].fillna(df[col].mean(), inplace=True)
    
    # Convert dates
    df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], format='mixed')
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='mixed')
    
    # Convert time
    df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4)
    df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H%M').dt.time
    
    # Convert numeric columns to integers
    for col in num_cols:
        df[col] = df[col].astype(np.int64)
    
    # Extract year and month
    df['occ_year'] = df['DATE OCC'].dt.year
    df['occ_month'] = df['DATE OCC'].dt.month
    
    # Extract day of week
    df['Day of Week'] = df['Date Rptd'].dt.day_name()
    
    return df

def normalize_data(df):
    """Normalize numerical data."""
    def norm(column):
        max_min = column.max() - column.min()
        return (column - column.min()) / max_min
    
    # Apply normalization to columns that don't follow normal distribution
    for col in df.columns:
        if df[col].dtype == np.int64:
            stat, p_value = shapiro(df[col])
            if p_value < 0.05:
                df[col] = norm(df[col])
    
    return df

def encode_categorical(df):
    """Encode categorical variables."""
    categorical_cols = ['AREA NAME', 'Crm Cd Desc', 'Mocodes', 'Vict Sex', 
                      'Vict Descent', 'Premis Desc', 'Weapon Desc', 
                      'Status', 'Status Desc', 'LOCATION']
    
    le = LabelEncoder()
    df_enc = df.copy()
    
    for col in categorical_cols:
        df_enc[col] = le.fit_transform(df_enc[col])
    
    return df_enc