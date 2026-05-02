import polars as pl
import streamlit as st
import duckdb

from contextlib import contextmanager

DB_PATH = st.secrets['DB_PATH']

@contextmanager
def get_db_connection():
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        yield con
    finally:
        con.close()

@st.cache_data(show_spinner="Loading sales performance data...")
def get_sales_performance() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_sales_performance 
            ORDER BY order_date
            """).pl()
    
@st.cache_data(show_spinner="Loading geographic data...")
def get_customer_geography() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_customer_geography
            """).pl()
    
@st.cache_data(show_spinner="Loading product categories data...")
def get_product_categories() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_product_categories
            """).pl()
    
@st.cache_data(show_spinner="Loading reviews and satisfaction data...")
def get_reviews_satisfaction() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_reviews_and_satisfaction
            """).pl()
    
def load_css():
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    @media (prefers-color-scheme: dark) {
        div[data-testid="metric-container"] {
            background-color: #1e1e1e;
            border: 1px solid #333;
        }
    }
    </style>
    """, unsafe_allow_html=True)