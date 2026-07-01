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

@st.cache_data(ttl=3600, show_spinner="Loading sales performance data...")
def get_sales_performance() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_sales_performance 
            ORDER BY order_date
            """).pl()
    
@st.cache_data(ttl=3600, show_spinner="Loading geographic data...")
def get_customer_geography() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_customer_geography
            """).pl()
    
@st.cache_data(ttl=3600, show_spinner="Loading product categories data...")
def get_product_categories() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_product_categories
            """).pl()
    
@st.cache_data(ttl=3600, show_spinner="Loading reviews and satisfaction data...")
def get_reviews_satisfaction() -> pl.DataFrame:
    with get_db_connection() as session:
        return session.execute("""
            SELECT * 
            FROM mart.mart_reviews_and_satisfaction
            """).pl()

@st.cache_data(ttl=3600, show_spinner="Calculating top categories...")
def get_top_categories_by_revenue() -> pl.DataFrame:
    df_products = get_product_categories()
    
    top_categories = (
        df_products.group_by("product_category")
        .agg(pl.col("total_revenue").sum())
        .sort("total_revenue", descending=True)
        .head(8)
        .rename({"product_category": "Category", "total_revenue": "Revenue (BRL)"})
    )

    return top_categories.with_columns(
        pl.col("Category").str.replace_all("_", " ").str.to_titlecase()
    )

@st.cache_data(ttl=3600, show_spinner="Calculating delivery impact...")
def get_late_delivery_impact():
    df_reviews = get_reviews_satisfaction()
    score_by_lateness = (
        df_reviews.with_columns(
            pl.when(pl.col("is_late_delivery"))
            .then(pl.lit("Late Delivery"))
            .otherwise(pl.lit("On Time"))
            .alias("delivery_status")
        )
        .group_by("delivery_status")
        .agg(pl.col("review_score").mean())
    )
    
    on_time_df = score_by_lateness.filter(pl.col("delivery_status") == "On Time")
    late_df = score_by_lateness.filter(pl.col("delivery_status") == "Late Delivery")
    
    on_time_score = on_time_df["review_score"][0] if len(on_time_df) > 0 else 0.0
    late_score = late_df["review_score"][0] if len(late_df) > 0 else 0.0
    
    return on_time_score, late_score
    
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