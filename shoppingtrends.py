import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Customer Analytics Platform", layout="wide", page_icon="🛍️")

# ==========================
# HEADER IMAGE (optional)
# ==========================
image_path = "/mnt/data/teman-teman-wanita-keluar-berbelanja-bersama_53876-25041.avif"
if os.path.exists(image_path):
    st.image(Image.open(image_path), use_column_width=True)

st.title("📊 Customer Analytics Platform")

# ==========================
# LOAD FIXED DATASET
# ==========================
CSV_PATH = "df_EDA shopping.csv"

if not os.path.exists(CSV_PATH):
    st.error("❌ File 'df_EDA shopping.csv' tidak ditemukan di folder project!")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

# ==========================
# COLUMN TYPES
# ==========================
num_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

# ==========================
# SIDEBAR NAVIGATION
# ==========================
menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "General Dashboard",
        "EDA",
        "Customer Demographics",
        "Customer Spending",
        "Customer Satisfaction & Loyalty"
    ]
)

# ==========================
# MAIN APP
# ==========================

# ------------------------------------
# 1. GENERAL DASHBOARD
# ------------------------------------
if menu == "General Dashboard":
    st.header("📈 General Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", df.shape[0])
    c2.metric("Total Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))
    c4.metric("Numeric Features", len(num_cols))

    st.markdown("---")
    st.subheader("Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Quick Distribution")
    left, right = st.columns(2)

    with left:
        if num_cols:
            sel_num = st.selectbox("Pilih Numeric Column", num_cols)
            fig = px.histogram(df, x=sel_num, nbins=30, marginal="box")
            st.plotly_chart(fig, use_container_width=True)

    with right:
        if cat_cols:
            sel_cat = st.selectbox("Pilih Categorical Column", cat_cols)
            vc = df[sel_cat].value_counts().reset_index()
            vc.columns = [sel_cat, "Total"]
            fig = px.bar(vc, x=sel_cat, y="Total")
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------------

# 3. CUSTOMER DEMOGRAPHICS
# ------------------------------------
elif menu == "Customer Demographics":
    st.header("👥 Customer Demographics")

    if cat_cols:
        demo_cat = st.selectbox("Pilih Kolom Demografi (Categorical)", cat_cols)
        vc = df[demo_cat].value_counts().reset_index()
        vc.columns = [demo_cat, "Total"]
        fig = px.bar(vc, x=demo_cat, y="Total")
        st.plotly_chart(fig, use_container_width=True)

    if num_cols:
        demo_num = st.selectbox("Pilih Kolom Demografi (Numeric)", num_cols)
        fig = px.histogram(df, x=demo_num, nbins=30, marginal="box")
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------
# 4. CUSTOMER SPENDING
# ------------------------------------
elif menu == "Customer Spending":
    st.header("💰 Customer Spending Insights")

    if num_cols:
        spend_col = st.selectbox("Pilih Kolom Spending", num_cols)

        total_spend = df[spend_col].sum()
        avg_spend = df[spend_col].mean()
        max_spend = df[spend_col].max()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Spending", f"{total_spend:,.0f}")
        c2.metric("Average Spending", f"{avg_spend:,.2f}")
        c3.metric("Max Spending", f"{max_spend:,.0f}")

        fig = px.histogram(df, x=spend_col, nbins=40, marginal="box")
        st.plotly_chart(fig, use_container_width=True)

        if cat_cols:
            seg_col = st.selectbox("Segmentasi Berdasarkan", cat_cols)
            group = df.groupby(seg_col)[spend_col].mean().sort_values(ascending=False).reset_index()
            fig = px.bar(group, x=seg_col, y=spend_col)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------------
# 5. CUSTOMER SATISFACTION & LOYALTY
# ------------------------------------
elif menu == "Customer Satisfaction & Loyalty":
    st.header("⭐ Customer Satisfaction & Loyalty")

    if num_cols:
        sat_col = st.selectbox("Pilih Kolom Satisfaction Score", num_cols)
        avg_score = df[sat_col].mean()
        max_score = df[sat_col].max()
        min_score = df[sat_col].min()

        c1, c2, c3 = st.columns(3)
        c1.metric("Average Score", f"{avg_score:.2f}")
        c2.metric("Highest Score", f"{max_score:.2f}")
        c3.metric("Lowest Score", f"{min_score:.2f}")

        fig = px.histogram(df, x=sat_col, nbins=30)
        st.plotly_chart(fig, use_container_width=True)

    if cat_cols:
        loyal_col = st.selectbox("Pilih Kolom Loyalti", cat_cols)
        vc = df[loyal_col].value_counts().reset_index()
        vc.columns = [loyal_col, "Total"]
        fig = px.bar(vc, x=loyal_col, y="Total")
        st.plotly_chart(fig, use_container_width=True)
