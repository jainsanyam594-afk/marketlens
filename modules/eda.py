import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

ICON_LINK = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">'

def show_overview(df):
    st.markdown(ICON_LINK + "<h3><i class='ti ti-chart-bar'></i> Dataset Overview</h3>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records",    len(df))
    col2.metric("Unique Products",  df['Product Name'].nunique())
    col3.metric("Total Revenue",    f"Rs.{df['Total Revenue'].sum():,.0f}")
    st.dataframe(df.describe())

def show_monthly_trend(df):
    st.markdown(ICON_LINK + "<h3><i class='ti ti-trending-up'></i> Monthly Revenue Trend</h3>",
                unsafe_allow_html=True)
    monthly = df.groupby('MonthYear')['Total Revenue'].sum().reset_index()
    monthly = monthly.sort_values('MonthYear')

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(monthly['MonthYear'], monthly['Total Revenue'],
            marker='o', color='steelblue')
    ax.set_xlabel("Month-Year")
    ax.set_ylabel("Total Revenue (Rs.)")
    ax.set_title("Monthly Revenue Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def show_top_products(df):
    st.markdown(ICON_LINK + "<h3><i class='ti ti-award'></i> Top 10 Products by Revenue</h3>",
                unsafe_allow_html=True)
    top = df.groupby('Product Name')['Total Revenue'].sum().nlargest(10).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top, x='Total Revenue', y='Product Name',
                palette='Blues_r', ax=ax)
    ax.set_title("Top 10 Products by Revenue")
    plt.tight_layout()
    st.pyplot(fig)

def show_regional_chart(df):
    if 'Region' not in df.columns:
        return
    st.markdown(ICON_LINK + "<h3><i class='ti ti-map'></i> Revenue by Region</h3>",
                unsafe_allow_html=True)
    region_data = df.groupby('Region')['Total Revenue'].sum()

    fig, ax = plt.subplots()
    ax.pie(region_data, labels=region_data.index,
           autopct='%1.1f%%', startangle=140)
    ax.set_title("Regional Revenue Distribution")
    st.pyplot(fig)