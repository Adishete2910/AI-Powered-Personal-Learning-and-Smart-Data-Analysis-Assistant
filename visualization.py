"""
Visualization Module for Smart Data Analyst Agent
This module contains functions for generating visualizations from datasets.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional


# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')


def create_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create an interactive correlation heatmap using Plotly.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        return None
    
    corr_matrix = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Correlation Matrix Heatmap',
        xaxis_title='Features',
        yaxis_title='Features',
        height=600,
        width=800
    )
    
    return fig


def create_histogram(df: pd.DataFrame, column: str, nbins: int = 30) -> go.Figure:
    """
    Create an interactive histogram for a numeric column.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name for histogram
        nbins (int): Number of bins
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure(data=[
        go.Histogram(x=df[column].dropna(), nbinsx=nbins, name=column)
    ])
    
    fig.update_layout(
        title=f'Distribution of {column}',
        xaxis_title=column,
        yaxis_title='Frequency',
        showlegend=True,
        height=500
    )
    
    return fig


def create_bar_chart(df: pd.DataFrame, column: str) -> go.Figure:
    """
    Create an interactive bar chart for a categorical column.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name for bar chart
        
    Returns:
        go.Figure: Plotly figure object
    """
    value_counts = df[column].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(x=value_counts.index, y=value_counts.values, name=column)
    ])
    
    fig.update_layout(
        title=f'Value Counts of {column}',
        xaxis_title=column,
        yaxis_title='Count',
        showlegend=False,
        height=500
    )
    
    return fig


def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, 
                       color_col: Optional[str] = None) -> go.Figure:
    """
    Create an interactive scatter plot.
    
    Args:
        df (pd.DataFrame): Input dataframe
        x_col (str): Column name for X axis
        y_col (str): Column name for Y axis
        color_col (Optional[str]): Column name for color coding
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                    title=f'{x_col} vs {y_col}',
                    height=500)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    
    return fig


def create_box_plot(df: pd.DataFrame, column: str) -> go.Figure:
    """
    Create an interactive box plot.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name for box plot
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure(data=[
        go.Box(y=df[column].dropna(), name=column)
    ])
    
    fig.update_layout(
        title=f'Box Plot of {column}',
        yaxis_title=column,
        height=500
    )
    
    return fig


def create_line_chart(df: pd.DataFrame, x_col: str, y_cols: List[str]) -> go.Figure:
    """
    Create an interactive line chart.
    
    Args:
        df (pd.DataFrame): Input dataframe
        x_col (str): Column name for X axis
        y_cols (List[str]): Column names for Y axis
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=y_col
        ))
    
    fig.update_layout(
        title=f'{x_col} Over Time',
        xaxis_title=x_col,
        yaxis_title='Value',
        height=500,
        showlegend=True
    )
    
    return fig


def create_pie_chart(df: pd.DataFrame, column: str) -> go.Figure:
    """
    Create an interactive pie chart.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name for pie chart
        
    Returns:
        go.Figure: Plotly figure object
    """
    value_counts = df[column].value_counts()
    
    fig = go.Figure(data=[
        go.Pie(labels=value_counts.index, values=value_counts.values, 
               name=column)
    ])
    
    fig.update_layout(
        title=f'Distribution of {column}',
        height=500
    )
    
    return fig


def create_area_chart(df: pd.DataFrame, x_col: str, y_cols: List[str]) -> go.Figure:
    """
    Create an interactive area chart.
    
    Args:
        df (pd.DataFrame): Input dataframe
        x_col (str): Column name for X axis
        y_cols (List[str]): Column names for Y axis
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            fill='tonexty' if len(fig.data) > 0 else 'tozeroy',
            name=y_col
        ))
    
    fig.update_layout(
        title=f'Area Chart: {x_col}',
        xaxis_title=x_col,
        yaxis_title='Value',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_pair_plot(df: pd.DataFrame, numeric_cols: List[str]) -> go.Figure:
    """
    Create an interactive pair plot for numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        numeric_cols (List[str]): Numeric columns to plot
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Limit to first 4 columns to avoid too much complexity
    cols = numeric_cols[:4]
    
    fig = px.scatter_matrix(
        df[cols],
        title='Pair Plot Matrix',
        height=800,
        width=900,
        labels={col: col for col in cols}
    )
    
    return fig
