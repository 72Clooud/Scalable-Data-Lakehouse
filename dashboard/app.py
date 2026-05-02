import streamlit as st
import polars as pl
from utils import (
    get_sales_performance, 
    get_customer_geography, 
    get_product_categories, 
    get_reviews_satisfaction,
    load_css
)

st.set_page_config(page_title="E-commerce Analytics", page_icon=":bar_chart:", layout="wide")
load_css() 

st.title(":bar_chart: E-commerce Executive Dashboard")
st.markdown("Condensed view of key store metrics (KPIs).")

df_sales = get_sales_performance()
df_geo = get_customer_geography()
df_products = get_product_categories()
df_reviews = get_reviews_satisfaction()

total_revenue = df_sales['total_revenue'].sum()
total_orders = df_sales['total_orders'].sum()
avg_delivery = df_geo['delivery_time_days'].mean()
avg_score = df_reviews['review_score'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"{total_revenue:,.0f} BRL")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Delivery Time", f"{avg_delivery:.1f} Days")
col4.metric("Avg Customer Score", f"{avg_score:.2f} / 5.0")

st.divider() 

col_trend, col_prod = st.columns([6, 4])

with col_trend:
    st.subheader(":chart_with_upwards_trend: Daily Revenue Trend")
    sales_clean = df_sales.rename({"order_date": "Order Date", "total_revenue": "Revenue (BRL)"})
    st.line_chart(data=sales_clean, x='Order Date', y='Revenue (BRL)')

with col_prod:
    st.subheader(":package: Top Categories by Revenue")
    
    top_categories = (
        df_products.group_by("product_category")
        .agg(pl.col("total_revenue").sum())
        .sort("total_revenue", descending=True)
        .head(8)
        .rename({"product_category": "Category", "total_revenue": "Revenue (BRL)"})
    )

    top_categories = top_categories.with_columns(
        pl.col("Category").str.replace_all("_", " ").str.to_titlecase()
    )

    st.bar_chart(
        data=top_categories, 
        x="Revenue (BRL)", 
        y="Category", 
        horizontal=True,
    )

col_map, col_impact = st.columns([5, 5])

with col_map:
    st.subheader(":earth_americas: Customer Distribution")
    st.map(data=df_geo, latitude='lat', longitude='lng')

with col_impact:
    st.subheader(":star: The Cost of Late Deliveries")
    st.markdown("How do delivery delays impact customer satisfaction?")
    
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
    
    on_time_score = score_by_lateness.filter(pl.col("delivery_status") == "On Time")["review_score"][0]
    late_score = score_by_lateness.filter(pl.col("delivery_status") == "Late Delivery")["review_score"][0]
    
    score_drop = late_score - on_time_score
    
    m1, m2 = st.columns(2)
    m1.metric(label="Score (Delivered On Time)", value=f"{on_time_score:.2f} :star:")
    m2.metric(
        label="Score (Late Delivery)", 
        value=f"{late_score:.2f} :star:", 
        delta=f"{score_drop:.2f} points", 
        delta_color="inverse"
    )
    
    st.info("Business Insight: Delivery delays drastically reduce the store's rating. Logistics optimization is a priority to improve online reviews.")