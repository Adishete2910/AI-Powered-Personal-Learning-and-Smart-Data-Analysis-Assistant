"""
Chatbot Module for Smart Data Analyst Agent
This module handles AI-powered conversations about datasets using Google Gemini API.
"""

import google.generativeai as genai
import pandas as pd
from typing import Optional, List, Dict
import streamlit as st


class DatasetChatBot:
    """
    AI-powered chatbot for dataset analysis using Google Gemini API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the chatbot with API key.
        
        Args:
            api_key (str): Google Gemini API key
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.api_configured = True
        except Exception as e:
            self.api_configured = False
            self.error_message = str(e)
    
    def prepare_dataset_context(self, df: pd.DataFrame, max_rows: int = 5) -> str:
        """
        Prepare dataset context for the AI model.
        
        Args:
            df (pd.DataFrame): Input dataframe
            max_rows (int): Maximum rows to include in context
            
        Returns:
            str: Dataset context as string
        """
        # Basic statistics
        stats_text = f"""
Dataset Overview:
- Shape: {df.shape[0]} rows, {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Data Types: {df.dtypes.to_dict()}
- Missing Values: {df.isnull().sum().to_dict()}

Dataset Statistics:
{df.describe().to_string()}

First {min(max_rows, len(df))} rows:
{df.head(max_rows).to_string()}
"""
        return stats_text
    
    def ask_question(self, question: str, dataset_context: str, 
                    chat_history: List[Dict] = None) -> str:
        """
        Ask a question about the dataset using AI.
        
        Args:
            question (str): User's question
            dataset_context (str): Dataset context
            chat_history (List[Dict]): Previous conversation history
            
        Returns:
            str: AI-generated response
        """
        if not self.api_configured:
            return f"Error: API not configured. {self.error_message}"
        
        try:
            # Build conversation with context
            conversation_parts = []
            
            # Add system context
            conversation_parts.append(f"""You are an expert data analyst AI assistant. 
You have been provided with a dataset and are helping users understand and analyze it.

{dataset_context}

Please answer the following question based on the dataset context provided:""")
            
            # Add chat history if available
            if chat_history:
                for msg in chat_history[-5:]:  # Last 5 messages for context
                    if msg['role'] == 'user':
                        conversation_parts.append(f"User: {msg['content']}")
                    else:
                        conversation_parts.append(f"Assistant: {msg['content']}")
            
            # Add current question
            conversation_parts.append(f"User: {question}")
            
            full_prompt = "\n".join(conversation_parts)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_sample_prompts(self) -> List[str]:
        """
        Get sample prompts that users can ask.
        
        Returns:
            List[str]: List of sample prompts
        """
        return [
            "What are the key statistics of this dataset?",
            "Identify the most important features in this dataset.",
            "What patterns do you see in the data?",
            "Are there any outliers or anomalies I should be aware of?",
            "What correlations exist between variables?",
            "Provide insights about the distribution of values.",
            "What data quality issues should I address?",
            "Suggest actionable insights from this dataset.",
            "Which columns have the strongest relationships?",
            "Summarize the main characteristics of this dataset."
        ]
    
    def generate_summary(self, df: pd.DataFrame) -> str:
        """
        Generate an AI summary of the dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            str: AI-generated summary
        """
        if not self.api_configured:
            return "Error: API not configured"
        
        try:
            context = self.prepare_dataset_context(df)
            
            prompt = f"""Based on the following dataset, provide a comprehensive summary including:
1. Dataset overview
2. Key statistics
3. Data quality observations
4. Notable patterns or relationships
5. Recommendations for further analysis

{context}

Please provide a professional analysis suitable for a data analyst."""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def detect_data_issues(self, df: pd.DataFrame) -> str:
        """
        Use AI to detect potential data quality issues.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            str: AI analysis of data issues
        """
        if not self.api_configured:
            return "Error: API not configured"
        
        try:
            context = self.prepare_dataset_context(df)
            
            prompt = f"""Analyze the following dataset for potential data quality issues:
{context}

Please identify:
1. Missing or null values
2. Outliers or anomalies
3. Data type inconsistencies
4. Duplicate records
5. Unexpected patterns or values
6. Recommendations for data cleaning

Provide a professional assessment."""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_insights(self, df: pd.DataFrame) -> str:
        """
        Generate AI-powered insights from the dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            str: AI-generated insights
        """
        if not self.api_configured:
            return "Error: API not configured"
        
        try:
            context = self.prepare_dataset_context(df)
            
            prompt = f"""Based on the following dataset, generate actionable business insights:
{context}

Please provide:
1. Top 3-5 key findings
2. Trends and patterns
3. Potential business implications
4. Recommendations for action
5. Areas for deeper investigation

Format the response professionally."""
            
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"Error generating insights: {str(e)}"
