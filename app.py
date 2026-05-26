"""
Smart Data Analyst Agent - Main Application
A comprehensive AI-powered data analysis tool using Streamlit and Google Gemini API.

Features:
- Upload and preview CSV/Excel files
- Data cleaning (missing values, duplicates)
- Statistical analysis and visualizations
- AI-powered chatbot for data questions
- AI-generated insights and recommendations
- Export capabilities
- Dark mode support

Author: AI Assistant
Date: 2024
"""

import csv

import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None
    PDFPLUMBER_AVAILABLE = False

# Import custom modules
from data_cleaning import (
    detect_missing_values, remove_duplicates, handle_missing_values,
    get_dataset_statistics, get_correlation_matrix, normalize_numeric_columns
)
from visualization import (
    create_correlation_heatmap, create_histogram, create_bar_chart,
    create_scatter_plot, create_box_plot, create_line_chart,
    create_pie_chart, create_area_chart, create_pair_plot
)
from chatbot import DatasetChatBot
from insights import InsightGenerator


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Smart Data Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --bg-start: #09112f;
        --bg-mid: #14276f;
        --bg-end: #e7f0ff;
        --accent: #ff5c8a;
        --accent-alt: #20d0ff;
        --accent-soft: #7a8cff;
        --card-bg: rgba(255, 255, 255, 0.88);
        --card-glow: rgba(255, 92, 138, 0.16);
        --text-dark: #0f172a;
        --text-light: #f8fafc;
    }

    body, .main, .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, rgba(255, 92, 138, 0.24), transparent 26%),
                    radial-gradient(circle at bottom right, rgba(32, 208, 255, 0.24), transparent 20%),
                    linear-gradient(180deg, var(--bg-start) 0%, var(--bg-mid) 45%, rgba(231, 240, 255, 0.96) 100%);
        color: var(--text-dark);
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #09142e 0%, #1d4492 100%) !important;
        color: var(--text-light);
        border-right: 1px solid rgba(255,255,255,0.12);
        padding-top: 1.2rem;
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }

    .sidebar-brand {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1.75rem;
        padding: 1rem 1rem 1.2rem;
        border-radius: 1.8rem;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
    }

    .sidebar-brand .brand-mark {
        width: 58px;
        height: 58px;
        display: grid;
        place-items: center;
        border-radius: 18px;
        background: linear-gradient(135deg, #ff5c8a, #20d0ff);
        color: #ffffff;
        font-weight: 800;
        font-size: 1.1rem;
    }

    .sidebar-brand h2 {
        margin: 0;
        font-size: 1.2rem;
        line-height: 1.2;
        color: #ffffff;
    }

    .sidebar-brand p {
        margin: 0.35rem 0 0;
        color: rgba(255,255,255,0.78);
        font-size: 0.95rem;
    }

    .sidebar-card {
        background: rgba(255,255,255,0.08);
        border-radius: 1.4rem;
        padding: 1rem 1rem 1.1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.10);
    }

    .sidebar-card-title {
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.45rem;
        font-size: 1rem;
    }

    .sidebar-footer {
        padding: 1rem;
        border-radius: 1.5rem;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        color: rgba(255,255,255,0.78);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .page-header {
        padding: 1.75rem 1.75rem 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 2rem;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(255, 92, 138, 0.16);
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(18px);
    }

    .page-header h1 {
        margin-top: 0;
        font-size: 2.8rem;
        line-height: 1.05;
        letter-spacing: -0.05em;
        color: #081341;
    }

    .page-header p {
        margin: 1rem 0 0;
        font-size: 1rem;
        color: #334155;
        line-height: 1.75;
    }

    .hero-card, .gallery-card, .stDataFrame, .stTable, .stAlert, .stMetric {
        background: var(--card-bg) !important;
        border-radius: 1.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.30) !important;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.10) !important;
        backdrop-filter: blur(14px);
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(255, 92, 138, 0.95), rgba(32, 208, 255, 0.92)) !important;
        color: #ffffff;
        padding: 2rem;
        border-radius: 2rem;
        margin-bottom: 1.75rem;
    }

    .hero-card h2 {
        margin: 0;
        font-size: 2.4rem;
        line-height: 1.05;
        font-weight: 800;
    }

    .hero-card p {
        color: rgba(255,255,255,0.92);
        font-size: 1.05rem;
        line-height: 1.8;
        margin: 1rem 0 1.25rem;
    }

    .hero-card .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.85rem;
        margin-top: 1rem;
    }

    .hero-card .hero-badges span {
        background: rgba(255,255,255,0.18);
        padding: 0.7rem 1.1rem;
        border-radius: 999px;
        font-size: 0.95rem;
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.22);
    }

    .hero-banner {
        background-image: linear-gradient(135deg, rgba(255, 92, 138, 0.80), rgba(32, 208, 255, 0.80)),
                          url('https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1400&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 2rem;
        overflow: hidden;
        margin-bottom: 1.75rem;
        position: relative;
        min-height: 360px;
    }

    .hero-banner::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(17, 24, 39, 0.20), rgba(17, 24, 39, 0.52));
    }

    .hero-banner-content {
        position: relative;
        z-index: 1;
        padding: 2.5rem;
        color: #ffffff;
    }

    .hero-banner h2 {
        margin: 0;
        font-size: 2.6rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .hero-banner p {
        margin: 1rem 0 1.25rem;
        max-width: 720px;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.92);
        line-height: 1.8;
    }

    .hero-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .gallery-card {
        border-radius: 1.5rem;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255, 92, 138, 0.15);
        background: #ffffff;
    }

    .gallery-card img {
        width: 100%;
        display: block;
        object-fit: cover;
        height: 220px;
    }

    .gallery-card .caption {
        padding: 1rem;
        font-size: 0.95rem;
        color: #334155;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .feature-card {
        background: var(--card-bg);
        border-radius: 1.4rem;
        border: 1px solid rgba(255, 92, 138, 0.12);
        padding: 1.4rem;
        box-shadow: 0 16px 40px rgba(255, 92, 138, 0.08);
    }

    .feature-card h4 {
        margin: 0 0 0.5rem;
        font-size: 1.05rem;
        color: #ff5c8a;
    }

    .feature-card p {
        margin: 0;
        color: #334155;
        line-height: 1.7;
    }

    .stButton>button, .stDownloadButton>button {
        border-radius: 999px !important;
        border: none !important;
        box-shadow: 0 16px 40px rgba(255, 92, 138, 0.18) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
        background: linear-gradient(135deg, #ff5c8a, #20d0ff) !important;
        color: #ffffff !important;
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px);
        filter: brightness(1.08);
    }

    .stTextInput>div>input, .stSelectbox>div>div>div>div, .stTextArea>div>textarea {
        border-radius: 1rem;
        border: 1px solid rgba(255, 92, 138, 0.16) !important;
        background: rgba(255,255,255,0.96) !important;
    }

    .stFileUploader {
        border-radius: 1.5rem !important;
        border: 1px solid rgba(255, 92, 138, 0.18) !important;
        background: rgba(255,255,255,0.95) !important;
        padding: 0.9rem !important;
    }

    .stRadio>label, .stCheckbox>label {
        color: #f8fafc !important;
    }

    .stTextInput>label, .stTextArea>label, .stSelectbox>label {
        color: #f8fafc !important;
    }

    .stTabs [role="tablist"] button {
        border-radius: 999px !important;
    }

    .stAlert {
        border-radius: 1.4rem !important;
    }

    .stMetric {
        border-radius: 1.4rem !important;
    }

    @media (max-width: 900px) {
        .hero-card, .section-card, .sidebar-brand, .sidebar-card {
            border-radius: 1.4rem;
        }

        .hero-card h2 {
            font-size: 2rem;
        }

        .hero-banner {
            min-height: 260px;
        }

        .gallery-grid, .feature-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE INITIALIZATION ====================

def initialize_session_state():
    """Initialize all session state variables."""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'gemini_key' not in st.session_state:
        st.session_state.gemini_key = ""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"
    if 'adv_image' not in st.session_state:
        st.session_state.adv_image = None


initialize_session_state()


def render_sidebar():
    """Render the premium sidebar with branding, navigation, and API configuration."""
    with st.sidebar:
        st.markdown(
            """
            <div class='sidebar-brand'>
                <div class='brand-mark'>AI</div>
                <div>
                    <h2>AnyList AI Analyst</h2>
                    <p>Premium AI data workspace for powerful analytics.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigate to",
            [
                "🏠 Home",
                "📤 Upload Data",
                "🔍 Data Overview",
                "🧹 Data Cleaning",
                "📈 Visualizations",
                "🤖 AI Chatbot",
                "💡 Insights & Recommendations",
                "⚙️ Settings"
            ],
            key='page'
        )

        st.markdown("<div class='sidebar-card'><p class='sidebar-card-title'>Secure API Key</p><p>Store your Gemini API key safely in session state.</p></div>", unsafe_allow_html=True)
        api_key = st.text_input(
            "Google Gemini API Key:",
            value=st.session_state.gemini_key,
            type="password",
            help="Get your API key from https://makersuite.google.com/"
        )

        if api_key and api_key != st.session_state.gemini_key:
            st.session_state.gemini_key = api_key
            try:
                st.session_state.chatbot = DatasetChatBot(api_key)
                st.success("✅ API Key configured!")
            except Exception as e:
                st.session_state.chatbot = None
                st.error(f"❌ Failed to configure Gemini chatbot: {str(e)}")

        if st.session_state.gemini_key and st.session_state.chatbot is None:
            try:
                st.session_state.chatbot = DatasetChatBot(st.session_state.gemini_key)
            except Exception as e:
                st.session_state.chatbot = None
                st.error(f"❌ Failed to initialize Gemini chatbot: {str(e)}")

        st.markdown("""
            <div class='sidebar-card'>
                <p class='sidebar-card-title'>Project</p>
                <p>Visual analytics, AI chat, clean data exports, and smart insights all in one dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""
            <div class='sidebar-footer'>
                <strong>Need help?</strong> Use the AI Chatbot section to ask questions about your dataset.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


# Safe Gemini initialization from Streamlit secrets
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    if API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
except Exception as e:
    # Streamlit should still start even if Gemini is unavailable.
    st.warning(f"Gemini AI could not initialize: {str(e)}")


# ==================== UTILITY FUNCTIONS ====================

def load_pdf_dataset(uploaded_file) -> pd.DataFrame:
    """
    Load tabular data from a PDF file.
    """
    if not PDFPLUMBER_AVAILABLE:
        st.error(
            "❌ PDF import is currently unavailable because the required library is not installed. "
            "Please upload a CSV or Excel file instead."
        )
        return None

    try:
        file_bytes = uploaded_file.read()
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        if table and len(table) > 1:
                            cleaned_rows = [
                                [str(cell).strip() if cell is not None else "" for cell in row]
                                for row in table
                                if any(cell is not None and str(cell).strip() for cell in row)
                            ]
                            if len(cleaned_rows) <= 1:
                                continue
                            header = cleaned_rows[0]
                            rows = cleaned_rows[1:]
                            df_table = pd.DataFrame(rows, columns=header)
                            tables.append(df_table)

            if tables:
                return pd.concat(tables, ignore_index=True)

            # Fallback: try text extraction and split into columns
            fallback_tables = []
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                if len(lines) < 2:
                    continue

                rows = []
                if any('\t' in line for line in lines):
                    rows = [line.split('\t') for line in lines]
                else:
                    rows = [re.split(r'\s{2,}', line) for line in lines]

                if len(rows) > 1 and all(len(row) == len(rows[0]) for row in rows[:min(5, len(rows))]):
                    fallback_tables.append(pd.DataFrame(rows[1:], columns=rows[0]))

            if fallback_tables:
                return pd.concat(fallback_tables, ignore_index=True)

            st.error(
                "❌ No extractable tables were found in this PDF. "
                "If the file is scanned or image-based, convert it to CSV/Excel first."
            )
            return None
    except Exception as e:
        st.error(f"❌ Error loading PDF: {str(e)}")
        return None


def load_dataset(uploaded_file) -> pd.DataFrame:
    """
    Load dataset from uploaded file (CSV, Excel, or PDF).
    
    Args:
        uploaded_file: File uploaded through Streamlit
        
    Returns:
        pd.DataFrame: Loaded dataset or None if error
    """
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        elif filename.endswith('.pdf'):
            df = load_pdf_dataset(uploaded_file)
        else:
            st.error("❌ Unsupported file format. Please upload CSV, Excel, or PDF file.")
            return None

        if df is not None:
            st.success(f"✅ Successfully loaded: {uploaded_file.name}")
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None


def export_to_csv(df: pd.DataFrame, filename: str = "cleaned_dataset.csv") -> bytes:
    """
    Export dataframe to CSV format.
    
    Args:
        df (pd.DataFrame): Dataframe to export
        filename (str): Output filename
        
    Returns:
        bytes: CSV file in bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(df: pd.DataFrame, filename: str = "cleaned_dataset.xlsx") -> bytes:
    """
    Export dataframe to Excel format.
    
    Args:
        df (pd.DataFrame): Dataframe to export
        filename (str): Output filename
        
    Returns:
        bytes: Excel file in bytes
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        
        # Add statistics sheet
        stats_df = df.describe().T
        stats_df.to_excel(writer, sheet_name='Statistics')
    
    return output.getvalue()


def generate_report(df: pd.DataFrame, insights_gen: InsightGenerator) -> str:
    """
    Generate a comprehensive analysis report.
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        insights_gen (InsightGenerator): Insights generator instance
        
    Returns:
        str: Formatted report text
    """
    report = []
    report.append("=" * 80)
    report.append("DATA ANALYSIS REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")
    
    # Dataset Overview
    report.append("1. DATASET OVERVIEW")
    report.append("-" * 40)
    basic_insights = insights_gen.get_basic_insights(df)
    report.append(f"Total Records: {basic_insights['total_records']}")
    report.append(f"Total Features: {basic_insights['total_features']}")
    report.append(f"Numeric Features: {basic_insights['numeric_features']}")
    report.append(f"Categorical Features: {basic_insights['categorical_features']}")
    report.append(f"Missing Data: {basic_insights['missing_data_percentage']:.2f}%")
    report.append(f"Duplicate Rows: {basic_insights['duplicate_rows']}")
    report.append("")
    
    # Data Quality
    report.append("2. DATA QUALITY SCORE")
    report.append("-" * 40)
    quality_score = insights_gen.get_data_quality_score(df)
    report.append(f"Quality Score: {quality_score}/100")
    report.append("")
    
    # Correlation Analysis
    report.append("3. CORRELATION ANALYSIS")
    report.append("-" * 40)
    correlations = insights_gen.get_correlation_insights(df, threshold=0.5)
    if correlations:
        for col1, col2, corr in correlations[:5]:
            report.append(f"{col1} <-> {col2}: {corr}")
    else:
        report.append("No strong correlations found.")
    report.append("")
    
    # Recommendations
    report.append("4. RECOMMENDATIONS")
    report.append("-" * 40)
    recommendations = insights_gen.generate_recommendations(df)
    for rec in recommendations:
        report.append(f"• {rec}")
    
    return "\n".join(report)


# ==================== MAIN APP ====================

def main():
    """Main application function."""
    page = render_sidebar()

    # ==================== PAGE: HOME ====================
    if page == "🏠 Home":
        st.markdown(
            "<div class='page-header'><h1>AI-Powered Data Analyst Studio</h1><p>Modern analytics, clean data preparation, and intelligent recommendations in a premium dashboard experience.</p></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='hero-card'>
                <h2>Build a stunning analytics workspace for your datasets.</h2>
                <p>Upload, explore, clean, and ask your data questions with style. Designed for teams that want a polished AI-first experience at every step.</p>
                <div class='hero-badges'>
                    <span>Smart uploads</span>
                    <span>Interactive charts</span>
                    <span>AI recommendations</span>
                    <span>Modern dashboards</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([3, 1], gap="large")
        with col1:
            st.markdown("<div class='section-card'><h3>✨ What this app delivers</h3><p>Every feature is built to feel premium: from dataset onboarding and cleaning to insights, visual storytelling, and conversational AI support.</p></div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class='feature-grid'>
                    <div class='feature-card'>
                        <h4>Fast Upload</h4>
                        <p>Import CSV, Excel, or PDF datasets quickly with drag-and-drop style UI.</p>
                    </div>
                    <div class='feature-card'>
                        <h4>Clean Data</h4>
                        <p>Remove duplicates, handle missing values, and normalize with a few clicks.</p>
                    </div>
                    <div class='feature-card'>
                        <h4>Smart Insights</h4>
                        <p>Use AI-generated recommendations and quality scores to improve your data.</p>
                    </div>
                    <div class='feature-card'>
                        <h4>Visual Dashboards</h4>
                        <p>Explore charts, correlation maps, and pair plots that make trends obvious.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("<div class='section-card'><h3>📌 Quick Actions</h3><p>Navigate the workflow with quick action buttons and launch the features you need faster.</p></div>", unsafe_allow_html=True)
            if st.session_state.df is not None:
                st.metric("Rows", f"{st.session_state.df.shape[0]:,}")
                st.metric("Columns", f"{st.session_state.df.shape[1]:,}")
                st.metric("Loaded Files", f"{len(st.session_state.uploaded_files)}")
            else:
                st.metric("Rows", "--")
                st.metric("Columns", "--")
                st.metric("Loaded Files", "0")
            st.markdown("---")
            if st.button("🚀 Start Upload"):
                st.session_state.page = "📤 Upload Data"
                st.experimental_rerun()
            if st.button("📈 Explore Visuals"):
                st.session_state.page = "📈 Visualizations"
                st.experimental_rerun()

        st.markdown("<div class='section-header'>✅ Why users love it</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='gallery-grid'>
                <div class='gallery-card'>
                    <img src='https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1000&q=80' alt='Data Strategy'>
                    <div class='caption'>Beautiful dashboards that look premium and feel effortless.</div>
                </div>
                <div class='gallery-card'>
                    <img src='https://images.unsplash.com/photo-1525378960530-7c0da6231fb1?auto=format&fit=crop&w=1000&q=80' alt='Team Collaboration'>
                    <div class='caption'>Designed for collaboration, insight sharing, and executive storytelling.</div>
                </div>
                <div class='gallery-card'>
                    <img src='https://images.unsplash.com/photo-1551924540-1ba343ebc7fe?auto=format&fit=crop&w=1000&q=80' alt='AI Insights'>
                    <div class='caption'>AI-powered insights make your dataset feel faster and smarter.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # ==================== PAGE: UPLOAD DATA ====================
    elif page == "📤 Upload Data":
        st.markdown(
            "<div class='page-header'><h1>📤 Upload Dataset</h1><p>Easily import CSV, Excel, or PDF datasets and start your analytics workflow in seconds.</p></div>",
            unsafe_allow_html=True,
        )
        
        st.info(
            "💡 **Tip**: You can upload CSV, Excel, or PDF files. "
            "PDF files should contain tables for extraction."
        )
        
        uploaded_files = st.file_uploader(
            "Choose file(s) to upload:",
            type=["csv", "xlsx", "xls", "pdf"],
            accept_multiple_files=True,
            help="Upload CSV, Excel, or PDF files"
        )
        uploaded_files = st.session_state.uploaded_files + [f.name for f in uploaded_files if f.name not in st.session_state.uploaded_files]
        # choose one file of them
        # uploaded_files will be added to session state, and only the last one will be loaded as the current dataset.
        if uploaded_files:
            for uploaded_file in uploaded_files:
                df = load_dataset(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.original_df = df.copy()
                    st.session_state.uploaded_files.append(uploaded_file.name)
                    
                    st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
                    st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        if st.session_state.df is not None:
            st.markdown("---")
            st.markdown("### 📋 Currently Loaded Dataset")
            st.write(f"**File**: {', '.join(st.session_state.uploaded_files)}")
            st.write(f"**Shape**: {st.session_state.df.shape}")
    
    # ==================== PAGE: DATA OVERVIEW ====================
    elif page == "🔍 Data Overview":
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first in the '📤 Upload Data' section.")
            return
        
        df = st.session_state.df
        
        st.markdown(
            "<div class='page-header'><h1>🔍 Data Overview</h1><p>Explore your dataset with interactive summaries, quality metrics, and easy-to-read previews.</p></div>",
            unsafe_allow_html=True,
        )
        
        # Display basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Rows", f"{df.shape[0]:,}")
        with col2:
            st.metric("📈 Columns", df.shape[1])
        with col3:
            missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            st.metric("❌ Missing Values", f"{missing_pct:.1f}%")
        with col4:
            duplicates = df.duplicated().sum()
            st.metric("🔄 Duplicates", f"{duplicates:,}")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📋 Data Preview", "📊 Statistics", "🔍 Data Types", "📉 Missing Values"]
        )
        
        with tab1:
            st.markdown("### Dataset Preview")
            rows_to_show = st.slider("Rows to display:", 5, 100, 10)
            st.dataframe(df.head(rows_to_show), use_container_width=True)
        
        with tab2:
            st.markdown("### Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
        
        with tab3:
            st.markdown("### Data Types")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values
            })
            st.dataframe(dtype_df, use_container_width=True)
        
        with tab4:
            st.markdown("### Missing Values Analysis")
            missing_df = pd.DataFrame({
                'Column': df.columns,
                'Missing Count': df.isnull().sum().values,
                'Missing Percentage': ((df.isnull().sum() / len(df)) * 100).values
            })
            missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(
                'Missing Percentage', ascending=False
            )
            
            if len(missing_df) > 0:
                st.dataframe(missing_df, use_container_width=True)
            else:
                st.success("✅ No missing values found!")
    
    # ==================== PAGE: DATA CLEANING ====================
    elif page == "🧹 Data Cleaning":
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first in the '📤 Upload Data' section.")
            return
        
        df = st.session_state.df
        
        st.markdown(
            "<div class='page-header'><h1>🧹 Data Cleaning & Preprocessing</h1><p>Clean and normalize your dataset with powerful controls and instant preview feedback.</p></div>",
            unsafe_allow_html=True,
        )
        
        col1, col2 = st.columns(2)
        
        # Remove Duplicates
        with col1:
            st.markdown("### 🔄 Remove Duplicates")
            duplicates = df.duplicated().sum()
            st.write(f"Current duplicates: {duplicates}")
            
            if st.button("🗑️ Remove Duplicate Rows"):
                df_cleaned, removed = remove_duplicates(df)
                st.session_state.df = df_cleaned
                st.success(f"✅ Removed {removed} duplicate rows!")
                st.rerun()
        
        # Handle Missing Values
        with col2:
            st.markdown("### ❌ Handle Missing Values")
            missing_total = df.isnull().sum().sum()
            st.write(f"Current missing values: {missing_total}")
            
            strategy = st.selectbox(
                "Select strategy:",
                ["drop", "mean", "median", "forward_fill", "backward_fill"],
                help="drop: Remove rows with missing values\n"
                     "mean: Fill with column mean\n"
                     "median: Fill with column median\n"
                     "forward_fill: Propagate values forward\n"
                     "backward_fill: Propagate values backward"
            )
            
            columns_to_clean = st.multiselect(
                "Select columns to clean (leave empty for all):",
                df.columns.tolist()
            )
            
            if st.button("🧹 Apply Strategy"):
                columns = columns_to_clean if columns_to_clean else None
                df_cleaned = handle_missing_values(df, strategy=strategy, columns=columns)
                st.session_state.df = df_cleaned
                st.success("✅ Missing values handled successfully!")
                st.rerun()
        
        st.markdown("---")
        
        # Normalization
        st.markdown("### 📏 Normalize Numeric Columns")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            cols_to_normalize = st.multiselect(
                "Select columns to normalize:",
                numeric_cols
            )
            
            if st.button("⚖️ Normalize Selected Columns"):
                df_normalized = normalize_numeric_columns(df, columns=cols_to_normalize)
                st.session_state.df = df_normalized
                st.success("✅ Columns normalized successfully!")
                st.rerun()
        
        st.markdown("---")
        
        # Data Preview After Cleaning
        st.markdown("### 📋 Preview Cleaned Data")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        
        # Export Options
        st.markdown("### 💾 Export Cleaned Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = export_to_csv(st.session_state.df)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f"cleaned_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            excel_data = export_to_excel(st.session_state.df)
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name=f"cleaned_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # ==================== PAGE: VISUALIZATIONS ====================
    elif page == "📈 Visualizations":
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first in the '📤 Upload Data' section.")
            return
        
        df = st.session_state.df
        
        st.markdown(
            "<div class='page-header'><h1>📈 Interactive Visualizations</h1><p>Create modern, responsive charts and explore trends with intuitive visual controls.</p></div>",
            unsafe_allow_html=True,
        )
        st.info("Select a chart type below, then choose the fields to render the graph immediately.")
        
        viz_type = st.selectbox(
            "Select visualization type:",
            [
                "Correlation Heatmap",
                "Histogram",
                "Bar Chart",
                "Scatter Plot",
                "Box Plot",
                "Pie Chart",
                "Line Chart",
                "Area Chart",
                "Pair Plot"
            ]
        )
        
        try:
            # Correlation Heatmap
            if viz_type == "Correlation Heatmap":
                st.markdown("### 🔥 Correlation Matrix Heatmap")
                fig = create_correlation_heatmap(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No numeric columns found for correlation analysis.")
            
            # Histogram
            elif viz_type == "Histogram":
                st.markdown("### 📊 Histogram")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if numeric_cols:
                    selected_col = st.selectbox("Select column:", numeric_cols)
                    nbins = st.slider("Number of bins:", 5, 100, 30)
                    
                    fig = create_histogram(df, selected_col, nbins)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No numeric columns found.")
            
            # Bar Chart
            elif viz_type == "Bar Chart":
                st.markdown("### 📈 Bar Chart")
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                if categorical_cols:
                    selected_col = st.selectbox("Select column:", categorical_cols)
                    fig = create_bar_chart(df, selected_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No categorical columns found.")
            
            # Scatter Plot
            elif viz_type == "Scatter Plot":
                st.markdown("### 🔵 Scatter Plot")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                all_cols = df.columns.tolist()
                
                if len(numeric_cols) >= 2:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        x_col = st.selectbox("X-axis:", numeric_cols)
                    with col2:
                        y_col = st.selectbox("Y-axis:", numeric_cols)
                    with col3:
                        color_col = st.selectbox("Color by:", [None] + all_cols)
                    
                    fig = create_scatter_plot(df, x_col, y_col, color_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ At least 2 numeric columns required.")
            
            # Box Plot
            elif viz_type == "Box Plot":
                st.markdown("### 📦 Box Plot")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if numeric_cols:
                    selected_col = st.selectbox("Select column:", numeric_cols)
                    fig = create_box_plot(df, selected_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No numeric columns found.")
            
            # Pie Chart
            elif viz_type == "Pie Chart":
                st.markdown("### 🥧 Pie Chart")
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                if categorical_cols:
                    selected_col = st.selectbox("Select column:", categorical_cols)
                    fig = create_pie_chart(df, selected_col)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No categorical columns found.")
            
            # Line Chart
            elif viz_type == "Line Chart":
                st.markdown("### 📉 Line Chart")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X-axis:", df.columns.tolist())
                    y_cols = st.multiselect("Y-axis columns:", numeric_cols, default=numeric_cols[:2])
                    
                    if y_cols:
                        fig = create_line_chart(df, x_col, y_cols)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ At least 2 numeric columns required.")
            
            # Area Chart
            elif viz_type == "Area Chart":
                st.markdown("### 🌊 Area Chart")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X-axis:", df.columns.tolist())
                    y_cols = st.multiselect("Y-axis columns:", numeric_cols, default=numeric_cols[:2])
                    
                    if y_cols:
                        fig = create_area_chart(df, x_col, y_cols)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ At least 2 numeric columns required.")
            
            # Pair Plot
            elif viz_type == "Pair Plot":
                st.markdown("### 🔢 Pair Plot Matrix")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    fig = create_pair_plot(df, numeric_cols)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ At least 2 numeric columns required.")
        
        except Exception as e:
            st.error(f"❌ Error generating visualization: {str(e)}")
    
    # ==================== PAGE: AI CHATBOT ====================
    elif page == "🤖 AI Chatbot":
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first in the '📤 Upload Data' section.")
            return
        
        if not st.session_state.gemini_key:
            st.warning(
                "⚠️ Please configure your Google Gemini API key in the sidebar.\n\n"
                "Get one for free at https://makersuite.google.com/"
            )
            return
        
        st.markdown(
            "<div class='page-header'><h1>🤖 AI Data Chatbot</h1><p>Chat with your data in a clean conversational interface and get fast answers from AI.</p></div>",
            unsafe_allow_html=True,
        )
        
        df = st.session_state.df
        chatbot = st.session_state.chatbot
        
        if chatbot is None or not chatbot.api_configured:
            st.error("❌ Chatbot not properly configured. Please check your API key.")
            return
        
        # Display sample prompts
        st.markdown("### 💬 Sample Questions You Can Ask")
        
        col1, col2 = st.columns(2)
        sample_prompts = chatbot.get_sample_prompts()
        
        for i, prompt in enumerate(sample_prompts):
            if i < len(sample_prompts) // 2:
                with col1:
                    if st.button(f"💭 {prompt}", key=f"prompt_{i}"):
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': prompt
                        })
            else:
                with col2:
                    if st.button(f"💭 {prompt}", key=f"prompt_{i}"):
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': prompt
                        })
        
        st.markdown("---")
        
        # Chat Interface
        st.markdown("### 💬 Chat Interface")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.chat_message("user").write(msg['content'])
            else:
                st.chat_message("assistant").write(msg['content'])
        
        # User input
        user_input = st.chat_input("Ask a question about your dataset...")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Generate response
            with st.spinner("🤖 Thinking..."):
                dataset_context = chatbot.prepare_dataset_context(df)
                response = chatbot.ask_question(
                    user_input,
                    dataset_context,
                    st.session_state.chat_history[:-1]  # Exclude current message
                )
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            
            st.rerun()
    
    # ==================== PAGE: INSIGHTS ====================
    elif page == "💡 Insights & Recommendations":
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first in the '📤 Upload Data' section.")
            return
        
        df = st.session_state.df
        insights_gen = InsightGenerator()
        
        st.markdown(
            "<div class='page-header'><h1>💡 Insights & Recommendations</h1><p>Receive smart analysis, correlation highlights, and data improvement suggestions.</p></div>",
            unsafe_allow_html=True,
        )
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "🔗 Correlations", "📉 Distribution", "🎯 Outliers", "📋 Report"]
        )
        
        with tab1:
            st.markdown("### 📊 Dataset Overview")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            basic_insights = insights_gen.get_basic_insights(df)
            
            with col1:
                st.metric("Total Records", f"{basic_insights['total_records']:,}")
            with col2:
                st.metric("Total Features", basic_insights['total_features'])
            with col3:
                st.metric("Numeric Features", basic_insights['numeric_features'])
            with col4:
                st.metric("Categorical Features", basic_insights['categorical_features'])
            with col5:
                quality_score = insights_gen.get_data_quality_score(df)
                st.metric("Quality Score", f"{quality_score}/100")
            
            st.markdown("---")
            
            # Recommendations
            st.markdown("### 🎯 Recommendations")
            recommendations = insights_gen.generate_recommendations(df)
            for rec in recommendations:
                st.info(rec)
        
        with tab2:
            st.markdown("### 🔗 Correlation Analysis")
            
            threshold = st.slider("Correlation Threshold:", 0.0, 1.0, 0.7, 0.05)
            correlations = insights_gen.get_correlation_insights(df, threshold=threshold)
            
            if correlations:
                corr_df = pd.DataFrame(
                    correlations,
                    columns=['Feature 1', 'Feature 2', 'Correlation']
                )
                st.dataframe(corr_df, use_container_width=True)
            else:
                st.info("No strong correlations found above the threshold.")
        
        with tab3:
            st.markdown("### 📉 Distribution Analysis")
            
            dist_insights = insights_gen.get_distribution_insights(df)
            
            if dist_insights:
                dist_df = pd.DataFrame({
                    'Column': list(dist_insights.keys()),
                    'Distribution Type': [v['distribution_type'] for v in dist_insights.values()],
                    'Skewness': [v['skewness'] for v in dist_insights.values()],
                    'Kurtosis': [v['kurtosis'] for v in dist_insights.values()]
                })
                st.dataframe(dist_df, use_container_width=True)
            else:
                st.info("No numeric columns for distribution analysis.")
        
        with tab4:
            st.markdown("### 🎯 Outlier Detection")
            
            outlier_insights = insights_gen.get_outlier_insights(df)
            
            if outlier_insights:
                outlier_df = pd.DataFrame({
                    'Column': list(outlier_insights.keys()),
                    'Outlier Count': [v['outlier_count'] for v in outlier_insights.values()],
                    'Outlier %': [f"{v['outlier_percentage']:.2f}%" for v in outlier_insights.values()],
                    'Lower Bound': [v['lower_bound'] for v in outlier_insights.values()],
                    'Upper Bound': [v['upper_bound'] for v in outlier_insights.values()]
                })
                st.dataframe(outlier_df, use_container_width=True)
            else:
                st.info("No numeric columns for outlier detection.")
        
        with tab5:
            st.markdown("### 📋 Analysis Report")
            
            report = generate_report(df, insights_gen)
            st.text(report)
            
            # Download Report
            report_bytes = report.encode('utf-8')
            st.download_button(
                label="📥 Download Report as Text",
                data=report_bytes,
                file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # AI Insights (if API configured)
        if st.session_state.gemini_key and st.session_state.chatbot:
            st.markdown("---")
            st.markdown("### 🤖 AI-Generated Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Generate Data Summary"):
                    with st.spinner("Generating summary..."):
                        summary = st.session_state.chatbot.generate_summary(df)
                        st.info(summary)
            
            with col2:
                if st.button("⚠️ Detect Data Issues"):
                    with st.spinner("Analyzing data..."):
                        issues = st.session_state.chatbot.detect_data_issues(df)
                        st.warning(issues)
            
            if st.button("💡 Generate Business Insights"):
                with st.spinner("Generating insights..."):
                    insights_text = st.session_state.chatbot.generate_insights(df)
                    st.success(insights_text)
    
    # ==================== PAGE: SETTINGS ====================
    elif page == "⚙️ Settings":
        st.markdown(
            "<div class='page-header'><h1>⚙️ Settings & Configuration</h1><p>Tune your analytics experience, manage datasets, and control AI options in one place.</p></div>",
            unsafe_allow_html=True,
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎨 Theme Settings")
            theme = st.selectbox(
                "Select theme:",
                ["Light", "Dark", "Auto"]
            )
            st.info(f"Currently using: {theme} theme")
        
        with col2:
            st.markdown("### 📊 Visualization Settings")
            chart_type = st.selectbox(
                "Default chart library:",
                ["Plotly", "Matplotlib"]
            )
        
        st.markdown("---")
        
        st.markdown("### 📁 Data Management")
        
        if st.session_state.df is not None:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Reset to Original"):
                    st.session_state.df = st.session_state.original_df.copy()
                    st.success("✅ Data reset to original!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Clear Dataset"):
                    st.session_state.df = None
                    st.session_state.original_df = None
                    st.session_state.chat_history = []
                    st.success("✅ Dataset cleared!")
                    st.rerun()
            
            with col3:
                if st.button("🔄 Clear Chat History"):
                    st.session_state.chat_history = []
                    st.success("✅ Chat history cleared!")
                    st.rerun()
        else:
            st.info("📌 No dataset loaded. Upload data to see management options.")
        
        st.markdown("---")
        
        st.markdown("### 🔐 API Configuration")
        st.info(
            "**Google Gemini API**\n\n"
            "This application uses Google's Gemini API for AI-powered features.\n\n"
            "1. Visit https://makersuite.google.com/\n"
            "2. Create a new API key\n"
            "3. Enter it in the sidebar\n"
            "4. Your key is stored in the session (not saved)"
        )
        
        if st.session_state.gemini_key:
            st.success("✅ API Key configured and active")
        else:
            st.warning("⚠️ API Key not configured. Add it in the sidebar to enable AI features.")


# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    main()
