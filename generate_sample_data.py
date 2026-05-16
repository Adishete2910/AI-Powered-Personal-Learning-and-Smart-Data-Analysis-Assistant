"""
Sample Data Generator for Smart Data Analyst Agent
Generates test datasets to explore the application features without external data.

Usage:
    python generate_sample_data.py
    
This creates sample CSV and Excel files that can be used for testing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_sales_data(rows=1000):
    """
    Generate sample sales data.
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        pd.DataFrame: Sales dataset
    """
    np.random.seed(42)
    
    data = {
        'Date': [datetime(2023, 1, 1) + timedelta(days=x) for x in range(rows)],
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'], rows),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], rows),
        'Sales': np.random.randint(100, 5000, rows),
        'Quantity': np.random.randint(1, 50, rows),
        'Profit': np.random.randint(-500, 2000, rows),
        'Customer_Age': np.random.randint(18, 70, rows),
        'Customer_Satisfaction': np.random.uniform(1, 5, rows).round(2),
    }
    
    # Add some missing values
    for col in ['Profit', 'Customer_Satisfaction']:
        missing_indices = np.random.choice(rows, int(rows * 0.05), replace=False)
        for idx in missing_indices:
            data[col][idx] = np.nan
    
    # Add duplicates
    duplicate_rows = data.copy()
    for key in duplicate_rows:
        if isinstance(duplicate_rows[key], list):
            duplicate_rows[key] = duplicate_rows[key][:10]
    
    df = pd.DataFrame(data)
    return df


def generate_student_data(rows=500):
    """
    Generate sample student performance data.
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        pd.DataFrame: Student dataset
    """
    np.random.seed(42)
    
    data = {
        'Student_ID': range(1, rows + 1),
        'Name': [f'Student_{i}' for i in range(1, rows + 1)],
        'Grade': np.random.choice(['A', 'B', 'C', 'D', 'F'], rows),
        'Math_Score': np.random.randint(30, 100, rows),
        'English_Score': np.random.randint(30, 100, rows),
        'Science_Score': np.random.randint(30, 100, rows),
        'Attendance_Rate': np.random.uniform(60, 100, rows).round(2),
        'Study_Hours': np.random.uniform(1, 8, rows).round(1),
        'Parent_Education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], rows),
    }
    
    # Add some missing values
    for col in ['Attendance_Rate', 'Study_Hours']:
        missing_indices = np.random.choice(rows, int(rows * 0.1), replace=False)
        data[col] = pd.Series(data[col]).copy()
        data[col].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    return df


def generate_weather_data(rows=365):
    """
    Generate sample weather data.
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        pd.DataFrame: Weather dataset
    """
    np.random.seed(42)
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(rows)]
    
    data = {
        'Date': dates,
        'Temperature': np.random.uniform(5, 35, rows).round(1),
        'Humidity': np.random.uniform(20, 90, rows).round(1),
        'Wind_Speed': np.random.uniform(0, 30, rows).round(1),
        'Precipitation': np.random.uniform(0, 50, rows).round(1),
        'Visibility': np.random.uniform(0, 10, rows).round(1),
        'Cloud_Cover': np.random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Overcast'], rows),
        'Weather_Type': np.random.choice(['Sunny', 'Rainy', 'Cloudy', 'Snowy'], rows),
    }
    
    # Add missing values
    missing_indices = np.random.choice(rows, int(rows * 0.05), replace=False)
    data['Visibility'].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    return df


def generate_ecommerce_data(rows=800):
    """
    Generate sample e-commerce transaction data.
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        pd.DataFrame: E-commerce dataset
    """
    np.random.seed(42)
    
    data = {
        'Transaction_ID': range(1001, 1001 + rows),
        'Customer_ID': np.random.randint(1, 200, rows),
        'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], rows),
        'Order_Amount': np.random.uniform(10, 500, rows).round(2),
        'Shipping_Time': np.random.randint(1, 30, rows),
        'Delivery_Time': np.random.randint(2, 45, rows),
        'Payment_Method': np.random.choice(['Credit Card', 'PayPal', 'Debit Card', 'UPI'], rows),
        'Return_Status': np.random.choice(['Returned', 'Kept', 'Pending'], rows),
        'Customer_Rating': np.random.uniform(1, 5, rows).round(1),
    }
    
    # Add missing values
    missing_indices = np.random.choice(rows, int(rows * 0.08), replace=False)
    data['Customer_Rating'] = pd.Series(data['Customer_Rating'])
    data['Customer_Rating'].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    return df


def generate_healthcare_data(rows=600):
    """
    Generate sample healthcare patient data.
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        pd.DataFrame: Healthcare dataset
    """
    np.random.seed(42)
    
    data = {
        'Patient_ID': range(5001, 5001 + rows),
        'Age': np.random.randint(18, 85, rows),
        'Gender': np.random.choice(['Male', 'Female', 'Other'], rows),
        'BMI': np.random.uniform(15, 40, rows).round(1),
        'Blood_Pressure_Systolic': np.random.randint(90, 180, rows),
        'Blood_Pressure_Diastolic': np.random.randint(60, 110, rows),
        'Cholesterol': np.random.randint(120, 300, rows),
        'Disease_Status': np.random.choice(['Healthy', 'At Risk', 'Diagnosed'], rows),
        'Visit_Count': np.random.randint(0, 10, rows),
        'Medication_Count': np.random.randint(0, 8, rows),
    }
    
    # Add some missing values
    missing_indices = np.random.choice(rows, int(rows * 0.07), replace=False)
    data['Cholesterol'] = pd.Series(data['Cholesterol'])
    data['Cholesterol'].iloc[missing_indices] = np.nan
    
    df = pd.DataFrame(data)
    return df


def generate_all_samples():
    """Generate all sample datasets and save them."""
    
    print("🚀 Generating sample datasets...")
    print()
    
    # Create sample_data directory if it doesn't exist
    if not os.path.exists('sample_data'):
        os.makedirs('sample_data')
    
    # 1. Sales Data
    print("📊 Generating Sales Data...")
    sales_df = generate_sales_data(1000)
    sales_df.to_csv('sample_data/sales_data.csv', index=False)
    sales_df.to_excel('sample_data/sales_data.xlsx', index=False)
    print(f"   ✅ Created: sales_data.csv & sales_data.xlsx ({len(sales_df)} rows)")
    print(f"   Features: Date, Product, Region, Sales, Quantity, Profit, Customer_Age, Satisfaction")
    print()
    
    # 2. Student Data
    print("🎓 Generating Student Performance Data...")
    student_df = generate_student_data(500)
    student_df.to_csv('sample_data/student_data.csv', index=False)
    student_df.to_excel('sample_data/student_data.xlsx', index=False)
    print(f"   ✅ Created: student_data.csv & student_data.xlsx ({len(student_df)} rows)")
    print(f"   Features: Student_ID, Name, Grade, Scores, Attendance, Study_Hours, Parent_Education")
    print()
    
    # 3. Weather Data
    print("🌤️  Generating Weather Data...")
    weather_df = generate_weather_data(365)
    weather_df.to_csv('sample_data/weather_data.csv', index=False)
    weather_df.to_excel('sample_data/weather_data.xlsx', index=False)
    print(f"   ✅ Created: weather_data.csv & weather_data.xlsx ({len(weather_df)} rows)")
    print(f"   Features: Date, Temperature, Humidity, Wind_Speed, Precipitation, Visibility, Cloud_Cover")
    print()
    
    # 4. E-Commerce Data
    print("🛒 Generating E-Commerce Data...")
    ecommerce_df = generate_ecommerce_data(800)
    ecommerce_df.to_csv('sample_data/ecommerce_data.csv', index=False)
    ecommerce_df.to_excel('sample_data/ecommerce_data.xlsx', index=False)
    print(f"   ✅ Created: ecommerce_data.csv & ecommerce_data.xlsx ({len(ecommerce_df)} rows)")
    print(f"   Features: Transaction_ID, Customer_ID, Category, Amount, Times, Payment_Method, Rating")
    print()
    
    # 5. Healthcare Data
    print("🏥 Generating Healthcare Data...")
    healthcare_df = generate_healthcare_data(600)
    healthcare_df.to_csv('sample_data/healthcare_data.csv', index=False)
    healthcare_df.to_excel('sample_data/healthcare_data.xlsx', index=False)
    print(f"   ✅ Created: healthcare_data.csv & healthcare_data.xlsx ({len(healthcare_df)} rows)")
    print(f"   Features: Patient_ID, Age, Gender, BMI, Blood_Pressure, Cholesterol, Disease_Status")
    print()
    
    print("=" * 60)
    print("✨ All sample datasets generated successfully!")
    print("=" * 60)
    print()
    print("📁 Files created in 'sample_data/' directory:")
    print("   • sales_data.csv & .xlsx")
    print("   • student_data.csv & .xlsx")
    print("   • weather_data.csv & .xlsx")
    print("   • ecommerce_data.csv & .xlsx")
    print("   • healthcare_data.csv & .xlsx")
    print()
    print("🚀 Ready to test! Run: streamlit run app.py")
    print()


if __name__ == "__main__":
    generate_all_samples()
