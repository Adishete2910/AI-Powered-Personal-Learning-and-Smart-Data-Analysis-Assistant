# 🎨 Advanced Configuration Guide

Customize the Smart Data Analyst Agent to fit your needs.

---

## 📋 Table of Contents

1. [Theme Customization](#theme-customization)
2. [Feature Configuration](#feature-configuration)
3. [Performance Tuning](#performance-tuning)
4. [Integration Setup](#integration-setup)
5. [Advanced Features](#advanced-features)

---

## 🎨 Theme Customization

### Modify Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"      # Main blue
backgroundColor = "#ffffff"   # White background
secondaryBackgroundColor = "#f0f2f6"  # Light gray
textColor = "#262730"        # Dark text
font = "sans serif"
```

### Popular Color Schemes

#### Dark Theme
```toml
[theme]
primaryColor = "#00d4ff"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#161b22"
textColor = "#e6edf3"
```

#### Green Theme
```toml
[theme]
primaryColor = "#00b894"
backgroundColor = "#f5f5f5"
secondaryBackgroundColor = "#eaeaea"
textColor = "#2d3436"
```

#### Professional Blue
```toml
[theme]
primaryColor = "#003f87"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7f9fc"
textColor = "#1a1a1a"
```

---

## ⚙️ Feature Configuration

### Enable/Disable Features

Create `config.py`:

```python
# Feature toggles
FEATURES = {
    'data_upload': True,
    'data_cleaning': True,
    'visualizations': True,
    'ai_chatbot': True,
    'insights': True,
    'export': True,
}

# Data limits
MAX_UPLOAD_SIZE_MB = 500
MAX_ROWS_DISPLAY = 1000
MAX_CHART_POINTS = 10000

# API Configuration
GEMINI_MAX_TOKENS = 2048
GEMINI_TEMPERATURE = 0.7

# UI Settings
SIDEBAR_STATE = "expanded"  # or "collapsed"
PAGE_LAYOUT = "wide"  # or "centered"
INITIAL_SIDEBAR_STATE = "expanded"

# Advanced Features
ENABLE_ADVANCED_STATS = True
ENABLE_PAIR_PLOT = True
ENABLE_DARK_MODE = True
ENABLE_EXPORT_REPORT = True

# Cache Settings
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 3600
```

Then modify `app.py`:

```python
from config import FEATURES

# Use feature toggle
if FEATURES['ai_chatbot']:
    st.write("AI Chatbot Enabled")
```

---

## 🚀 Performance Tuning

### Cache Configuration

```toml
# .streamlit/config.toml
[client]
showErrorDetails = false
maxUploadSize = 200

[server]
maxUploadSize = 200
enableCORS = true
enableXsrfProtection = true

[logger]
level = "warning"
```

### Data Caching

```python
import streamlit as st
import pandas as pd

# Cache data loading
@st.cache_data(ttl=3600)
def load_dataset(uploaded_file):
    """Load and cache dataset for 1 hour"""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

# Cache heavy computations
@st.cache_data
def compute_correlations(df):
    """Cache correlation calculations"""
    return df.corr()
```

### Optimize Memory Usage

```python
# In app.py
import psutil
import os

def get_memory_usage():
    """Monitor memory usage"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

# Check before loading large files
if get_memory_usage() > 800:  # 800 MB threshold
    st.warning("⚠️ Memory usage high. Consider using smaller dataset.")
```

---

## 🔗 Integration Setup

### Database Integration

#### SQLite Example

```python
# db_connector.py
import sqlite3
import pandas as pd

class DatabaseConnector:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def get_table(self, table_name):
        return pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            self.conn
        )
    
    def save_table(self, df, table_name):
        df.to_sql(table_name, self.conn, if_exists='replace')

# In app.py
from db_connector import DatabaseConnector

db = DatabaseConnector('data.db')
df = db.get_table('my_data')
```

#### PostgreSQL Example

```python
# requirements.txt additions
psycopg2-binary==2.9.7

# db_connector.py
import psycopg2
import pandas as pd

class PostgresConnector:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
    
    def query(self, sql):
        return pd.read_sql_query(sql, self.conn)
```

### Cloud Storage Integration

#### Google Cloud Storage

```python
# In requirements.txt
google-cloud-storage==2.10.0

# In app.py
from google.cloud import storage

def upload_to_gcs(file_path, bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)

def download_from_gcs(bucket_name, blob_name, local_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_path)
```

#### AWS S3

```python
# In requirements.txt
boto3==1.28.0

# In app.py
import boto3

class S3Manager:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket = bucket_name
    
    def upload(self, file_path, key):
        self.s3.upload_file(file_path, self.bucket, key)
    
    def download(self, key, file_path):
        self.s3.download_file(self.bucket, key, file_path)
    
    def list_files(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket)
        return [obj['Key'] for obj in response.get('Contents', [])]
```

---

## 🌟 Advanced Features

### Custom Data Cleaning Functions

```python
# custom_cleaning.py
import pandas as pd
import numpy as np

def remove_outliers_zscore(df, column, threshold=3):
    """Remove outliers using z-score"""
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    return df[z_scores < threshold]

def encode_categorical(df, columns):
    """One-hot encode categorical columns"""
    return pd.get_dummies(df, columns=columns)

def impute_advanced(df, strategy='knn'):
    """Advanced imputation strategies"""
    from sklearn.impute import KNNImputer
    
    if strategy == 'knn':
        imputer = KNNImputer(n_neighbors=5)
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    
    return df
```

### Custom Visualizations

```python
# custom_visualizations.py
import plotly.graph_objects as go
import plotly.express as px

def create_3d_scatter(df, x_col, y_col, z_col, color_col=None):
    """Create 3D scatter plot"""
    fig = px.scatter_3d(
        df,
        x=x_col,
        y=y_col,
        z=z_col,
        color=color_col,
        title='3D Scatter Plot'
    )
    return fig

def create_sunburst(df, path_cols, values_col=None):
    """Create sunburst chart"""
    fig = px.sunburst(
        df,
        path=path_cols,
        values=values_col,
        title='Hierarchical Data'
    )
    return fig

def create_sankey(df, source_col, target_col, value_col):
    """Create Sankey diagram"""
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            line=dict(color='black', width=0.5),
            label=list(set(df[source_col].tolist() + df[target_col].tolist()))
        ),
        link=dict(
            source=df[source_col].astype('category').cat.codes,
            target=df[target_col].astype('category').cat.codes,
            value=df[value_col]
        )
    )])
    return fig
```

### Advanced ML Integration

```python
# ml_models.py
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd

class MLAnalytics:
    @staticmethod
    def clustering(df, n_clusters=3):
        """K-means clustering"""
        numeric_df = df.select_dtypes(include=['number'])
        kmeans = KMeans(n_clusters=n_clusters)
        clusters = kmeans.fit_predict(numeric_df)
        return clusters
    
    @staticmethod
    def dimensionality_reduction(df, n_components=2):
        """PCA dimensionality reduction"""
        numeric_df = df.select_dtypes(include=['number'])
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(numeric_df)
        return reduced
    
    @staticmethod
    def feature_importance(df, target_col):
        """Feature importance analysis"""
        from sklearn.ensemble import RandomForestClassifier
        
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        
        model = RandomForestClassifier()
        model.fit(X, y)
        
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
```

### User Authentication

```python
# auth.py
import streamlit_authenticator as stauth
import yaml
from pathlib import Path

def setup_authentication():
    """Setup user authentication"""
    
    # Create or load credentials
    credentials_path = Path('credentials.yaml')
    
    if not credentials_path.exists():
        config = {
            'credentials': {
                'usernames': {
                    'jsmith': {
                        'name': 'John Smith',
                        'password': 'password123'
                    }
                }
            }
        }
        with open(credentials_path, 'w') as f:
            yaml.dump(config, f)
    
    with open(credentials_path) as f:
        config = yaml.safe_load(f)
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        'data-analyst',
        'auth-key',
        cookie_expiry_days=30
    )
    
    return authenticator
```

---

## 📊 Custom Reports

```python
# report_generator.py
from datetime import datetime
import pandas as pd

class ReportGenerator:
    def __init__(self, df, title="Data Analysis Report"):
        self.df = df
        self.title = title
    
    def generate_html(self):
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.title}</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                h1 {{ color: #1f77b4; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #1f77b4; color: white; }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <h2>Dataset Summary</h2>
            <p>Rows: {len(self.df)}, Columns: {len(self.df.columns)}</p>
            <h2>Data Preview</h2>
            {self.df.head(10).to_html()}
            <h2>Statistics</h2>
            {self.df.describe().to_html()}
        </body>
        </html>
        """
        return html
    
    def save_html(self, filename):
        """Save report as HTML"""
        with open(filename, 'w') as f:
            f.write(self.generate_html())
```

---

## 🔐 Security Enhancements

### Input Validation

```python
# security.py
import re

def validate_filename(filename):
    """Validate uploaded filename"""
    # Allow only alphanumeric, dash, underscore, dot
    if not re.match(r'^[\w\-. ]+$', filename):
        raise ValueError("Invalid filename")
    return True

def sanitize_input(user_input):
    """Sanitize user input"""
    # Remove potentially dangerous characters
    return user_input.replace('<', '').replace('>', '').replace('"', '')
```

### Rate Limiting

```python
# In app.py
from datetime import datetime, timedelta
import streamlit as st

def check_rate_limit(key, max_requests=10, window_seconds=60):
    """Simple rate limiting"""
    if key not in st.session_state:
        st.session_state[key] = []
    
    now = datetime.now()
    cutoff = now - timedelta(seconds=window_seconds)
    
    # Remove old requests
    st.session_state[key] = [
        t for t in st.session_state[key] if t > cutoff
    ]
    
    if len(st.session_state[key]) < max_requests:
        st.session_state[key].append(now)
        return True
    
    return False
```

---

## 📈 Monitoring & Logging

```python
# monitoring.py
import logging
from datetime import datetime

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Usage in app
logger.info("User uploaded file")
logger.warning("Large file detected")
logger.error("API error occurred")
```

---

## 🎯 Summary

These configurations allow you to:
- ✅ Customize appearance
- ✅ Enable/disable features
- ✅ Optimize performance
- ✅ Integrate with databases
- ✅ Add advanced analytics
- ✅ Implement security
- ✅ Monitor usage

Start with basic customizations and gradually add advanced features as needed!

---

**Need help?** Check the main README.md or explore the code!
