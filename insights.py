"""
Insights Module for Smart Data Analyst Agent
This module generates insights and recommendations from datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import streamlit as st


class InsightGenerator:
    """
    Generate insights and recommendations from datasets.
    """
    
    @staticmethod
    def get_basic_insights(df: pd.DataFrame) -> Dict:
        """
        Generate basic insights about the dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Dictionary containing basic insights
        """
        insights = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'missing_data_percentage': (df.isnull().sum().sum() / 
                                       (len(df) * len(df.columns)) * 100),
            'duplicate_rows': df.duplicated().sum(),
            'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_features': len(df.select_dtypes(include=['object']).columns)
        }
        return insights
    
    @staticmethod
    def get_data_quality_score(df: pd.DataFrame) -> float:
        """
        Calculate a data quality score (0-100).
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            float: Data quality score
        """
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        # Calculate quality components
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        uniqueness = ((len(df) - duplicate_rows) / len(df)) * 100
        
        # Weighted average
        quality_score = (completeness * 0.7 + uniqueness * 0.3)
        
        return round(quality_score, 2)
    
    @staticmethod
    def get_column_insights(df: pd.DataFrame) -> Dict:
        """
        Generate insights for each column.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Column-wise insights
        """
        insights = {}
        
        for col in df.columns:
            col_insight = {
                'data_type': str(df[col].dtype),
                'missing_values': df[col].isnull().sum(),
                'missing_percentage': (df[col].isnull().sum() / len(df)) * 100,
                'unique_values': df[col].nunique()
            }
            
            # Numeric column insights
            if pd.api.types.is_numeric_dtype(df[col]):
                col_insight.update({
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std()
                })
            
            # Categorical column insights
            elif pd.api.types.is_object_dtype(df[col]):
                top_value = df[col].value_counts().index[0] if len(df[col].value_counts()) > 0 else None
                top_count = df[col].value_counts().values[0] if len(df[col].value_counts()) > 0 else 0
                col_insight.update({
                    'top_value': top_value,
                    'top_value_count': top_count,
                    'top_value_percentage': (top_count / len(df)) * 100
                })
            
            insights[col] = col_insight
        
        return insights
    
    @staticmethod
    def get_correlation_insights(df: pd.DataFrame, threshold: float = 0.7) -> List[Tuple[str, str, float]]:
        """
        Find strong correlations between numeric columns.
        
        Args:
            df (pd.DataFrame): Input dataframe
            threshold (float): Correlation threshold (0-1)
            
        Returns:
            List[Tuple[str, str, float]]: List of (col1, col2, correlation) tuples
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return []
        
        corr_matrix = numeric_df.corr().abs()
        
        # Get upper triangle of correlation matrix
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                if corr_value >= threshold:
                    corr_pairs.append((col1, col2, round(corr_value, 3)))
        
        # Sort by correlation value
        corr_pairs.sort(key=lambda x: x[2], reverse=True)
        return corr_pairs
    
    @staticmethod
    def get_distribution_insights(df: pd.DataFrame) -> Dict:
        """
        Analyze distribution of numeric columns.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Distribution insights
        """
        insights = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            skewness = df[col].skew()
            kurtosis = df[col].kurtosis()
            
            # Determine distribution type
            if abs(skewness) < 0.5:
                dist_type = "Approximately Symmetric"
            elif skewness > 0:
                dist_type = "Right-Skewed"
            else:
                dist_type = "Left-Skewed"
            
            insights[col] = {
                'distribution_type': dist_type,
                'skewness': round(skewness, 3),
                'kurtosis': round(kurtosis, 3)
            }
        
        return insights
    
    @staticmethod
    def get_outlier_insights(df: pd.DataFrame) -> Dict:
        """
        Detect and report outliers using IQR method.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Outlier information
        """
        insights = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_count = len(outliers)
            
            insights[col] = {
                'outlier_count': outlier_count,
                'outlier_percentage': (outlier_count / len(df)) * 100,
                'lower_bound': round(lower_bound, 3),
                'upper_bound': round(upper_bound, 3)
            }
        
        return insights
    
    @staticmethod
    def get_categorical_insights(df: pd.DataFrame) -> Dict:
        """
        Analyze categorical columns.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Categorical insights
        """
        insights = {}
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            
            insights[col] = {
                'unique_values': len(value_counts),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_count': value_counts.values[0] if len(value_counts) > 0 else 0,
                'least_common': value_counts.index[-1] if len(value_counts) > 0 else None,
                'least_common_count': value_counts.values[-1] if len(value_counts) > 0 else 0,
                'cardinality': len(value_counts) / len(df)  # Proportion of unique values
            }
        
        return insights
    
    @staticmethod
    def generate_recommendations(df: pd.DataFrame) -> List[str]:
        """
        Generate data analysis recommendations.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Check for missing values
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 10:
            recommendations.append(
                f"⚠️ Dataset has {missing_pct:.1f}% missing values. Consider data imputation strategies."
            )
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            recommendations.append(
                f"⚠️ Found {duplicates} duplicate rows. Consider removing them for cleaner analysis."
            )
        
        # Check for outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = len(df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)])
            
            if outliers > 0:
                recommendations.append(
                    f"📊 Column '{col}' has {outliers} potential outliers. Review these values."
                )
                break  # Limit to one outlier recommendation
        
        # Check for imbalanced data
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            if len(value_counts) > 1:
                max_count = value_counts.max()
                min_count = value_counts.min()
                ratio = max_count / min_count if min_count > 0 else float('inf')
                
                if ratio > 10:
                    recommendations.append(
                        f"⚠️ Column '{col}' shows class imbalance (ratio: {ratio:.1f}). Consider stratified analysis."
                    )
                    break
        
        if len(recommendations) == 0:
            recommendations.append(
                "✅ Dataset appears to be clean and well-structured. Proceed with analysis confidently."
            )
        
        return recommendations
