"""
Data Cleaning Module for Smart Data Analyst Agent
This module contains functions for cleaning and preprocessing datasets.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


def detect_missing_values(df: pd.DataFrame) -> Dict:
    """
    Detect missing values in the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        Dict: Dictionary containing missing value statistics
    """
    missing_stats = {
        'missing_count': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df)) * 100,
        'total_missing': df.isnull().sum().sum(),
        'total_cells': df.shape[0] * df.shape[1]
    }
    return missing_stats


def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> Tuple[pd.DataFrame, int]:
    """
    Remove duplicate rows from the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        subset (List[str]): Columns to consider for identifying duplicates
        
    Returns:
        Tuple[pd.DataFrame, int]: Cleaned dataframe and number of duplicates removed
    """
    initial_rows = len(df)
    df_cleaned = df.drop_duplicates(subset=subset)
    duplicates_removed = initial_rows - len(df_cleaned)
    return df_cleaned, duplicates_removed


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', 
                         columns: List[str] = None) -> pd.DataFrame:
    """
    Handle missing values using specified strategy.
    
    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): Strategy to use ('drop', 'mean', 'median', 'forward_fill', 'backward_fill')
        columns (List[str]): Specific columns to handle (None = all)
        
    Returns:
        pd.DataFrame: Dataframe with handled missing values
    """
    df_copy = df.copy()
    
    if columns is None:
        columns = df_copy.columns
    
    if strategy == 'drop':
        # Drop rows with any missing values in specified columns
        df_copy = df_copy.dropna(subset=columns)
    
    elif strategy == 'mean':
        # Fill with mean (only for numeric columns)
        numeric_cols = df_copy[columns].select_dtypes(include=[np.number]).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
    
    elif strategy == 'median':
        # Fill with median (only for numeric columns)
        numeric_cols = df_copy[columns].select_dtypes(include=[np.number]).columns
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
    
    elif strategy == 'forward_fill':
        # Forward fill
        df_copy[columns] = df_copy[columns].fillna(method='ffill')
    
    elif strategy == 'backward_fill':
        # Backward fill
        df_copy[columns] = df_copy[columns].fillna(method='bfill')
    
    return df_copy


def get_dataset_statistics(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive statistics for the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        Dict: Dictionary containing dataset statistics
    """
    stats = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'numeric_summary': df.describe().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # in MB
    }
    return stats


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr()


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
    """
    Detect outliers in a specific column.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name to check for outliers
        method (str): Method to use ('iqr' or 'zscore')
        
    Returns:
        pd.Series: Boolean series indicating outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        outliers = (df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))
    
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = z_scores > 3
    
    return outliers


def normalize_numeric_columns(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """
    Normalize numeric columns to 0-1 range.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (List[str]): Specific columns to normalize (None = all numeric)
        
    Returns:
        pd.DataFrame: Normalized dataframe
    """
    df_copy = df.copy()
    
    if columns is None:
        columns = df_copy.select_dtypes(include=[np.number]).columns
    
    for col in columns:
        if col in df_copy.columns:
            min_val = df_copy[col].min()
            max_val = df_copy[col].max()
            if max_val - min_val != 0:
                df_copy[col] = (df_copy[col] - min_val) / (max_val - min_val)
    
    return df_copy
