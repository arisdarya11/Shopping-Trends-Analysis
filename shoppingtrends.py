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
# SIDEBAR: NAV & UPLOAD
# ==========================
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "General Dashboard",
        "EDA",
        "Customer Demographics",
        "Customer Spending",
        "Customer Satisfaction & Loyalty"
    ],
)

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# optional: try load local default if tersedia
default_csv = "df_EDA shopping.csv"
data_source = None
if uploaded_file is not None:
    data_source = uploaded_file
elif os.path.exists(default_csv):
    data_source = default_csv

# ==========================
# LOAD DATA (cached)
# ==========================
@st.cache_data
def load_data(fp):
    try:
        return pd.read_csv(fp)
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        return None

df = None
if data_source is not None:
    df = load_data(data_source)

# ==========================
# UTILS
# ==========================
def get_num_cat_columns(df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    return num_cols, cat_cols

# ==========================
# MAIN APP
# ==========================
if df is not None and not df.empty:
    num_cols, cat_cols = get_num_cat_columns(df)

    # --------------------------
    # 1. GENERAL DASHBOARD
    # --------------------------
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
                sel_num = st.selectbox("Pilih Numeric Column (histogram)", num_cols, key="general_num")
                fig = px.histogram(df, x=sel_num, nbins=30, marginal="box", title=f"Distribusi: {sel_num}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada kolom numerik di dataset.")

        with right:
            if cat_cols:
                sel_cat = st.selectbox("Pilih Categorical Column (bar)", cat_cols, key="general_cat")
                vc = df[sel_cat].value_counts().reset_index()
                vc.columns = [sel_cat, "Total"]
                fig = px.bar(vc, x=sel_cat, y="Total", title=f"Frekuensi: {sel_cat}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada kolom kategorikal di dataset.")

    # --------------------------
    # 2. EDA
    # --------------------------
    elif menu == "EDA":
        st.header("🔍 Exploratory Data Analysis")
        st.subheader("Dataset Overview")
        st.dataframe(df.describe(include="all").T, use_container_width=True)

        st.subheader("Data Types & Missing")
        dt = pd.DataFrame({"dtype": df.dtypes.astype(str), "missing": df.isnull().sum()})
        st.dataframe(dt, use_container_width=True)

        if num_cols:
            st.subheader("Boxplot (Outlier Detection)")
            box_col = st.selectbox("Pilih kolom untuk boxplot", num_cols, key="eda_box")
            fig = px.box(df, y=box_col, points="outliers", title=f"Boxplot: {box_col}")
            st.plotly_chart(fig, use_container_width=True)

        if len(num_cols) > 1:
            st.subheader("Correlation Matrix")
            corr = df[num_cols].corr()
            fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

    # --------------------------
    # 3. CUSTOMER DEMOGRAPHICS
    # --------------------------
    elif menu == "Customer Demographics":
        st.header("👥 Customer Demographics Dashboard")

        if cat_cols:
            demo_col = st.selectbox("Pilih Kolom Demografi (categorical)", cat_cols, key="demo_cat")
            vc = df[demo_col].value_counts().reset_index()
            vc.columns = [demo_col, "Total"]
            fig = px.bar(vc, x=demo_col, y="Total", title=f"Distribusi: {demo_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada kolom kategorikal untuk demografi.")

        if num_cols:
            age_col = st.selectbox("Pilih Numeric Demographic", num_cols, key="demo_num")
            fig = px.histogram(df, x=age_col, nbins=30, title=f"Distribusi Numerik: {age_col}", marginal="box")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik untuk demografi.")

    # --------------------------
    # 4. CUSTOMER SPENDING
    # --------------------------
    elif menu == "Customer Spending":
        st.header("💰 Customer Spending Insights")

        if num_cols:
            spend_col = st.selectbox("Pilih Kolom Spending (numeric)", num_cols, key="spend_num")

            # KPI
            total_spend = df[spend_col].sum(skipna=True)
            avg_spend = df[spend_col].mean(skipna=True)
            max_spend = df[spend_col].max(skipna=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Spending", f"{total_spend:,.0f}")
            c2.metric("Average Spending", f"{avg_spend:,.2f}")
            c3.metric("Max Spending", f"{max_spend:,.0f}")

            st.markdown("---")
            fig = px.histogram(df, x=spend_col, nbins=40, title=f"Distribusi Spending: {spend_col}", marginal="box")
            st.plotly_chart(fig, use_container_width=True)

            if cat_cols:
                seg_col = st.selectbox("Segmentasi Berdasarkan (categorical)", cat_cols, key="spend_seg")
                group = df.groupby(seg_col)[spend_col].mean().sort_values(ascending=False).reset_index()
                group.columns = [seg_col, "AvgSpending"]
                fig = px.bar(group, x=seg_col, y="AvgSpending", title=f"Rata-rata {spend_col} per {seg_col}")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik untuk analisis spending.")

    # --------------------------
    # 5. CUSTOMER SATISFACTION & LOYALTY
    # --------------------------
    elif menu == "Customer Satisfaction & Loyalty":
        st.header("⭐ Customer Satisfaction & Loyalty")

        if num_cols:
            sat_col = st.selectbox("Pilih Kolom Satisfaction Score (numeric)", num_cols, key="sat_num")
            avg_score = df[sat_col].mean(skipna=True)
            max_score = df[sat_col].max(skipna=True)
            min_score = df[sat_col].min(skipna=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Average Score", f"{avg_score:.2f}")
            c2.metric("Highest Score", f"{max_score:.2f}")
            c3.metric("Lowest Score", f"{min_score:.2f}")

            fig = px.histogram(df, x=sat_col, nbins=30, title=f"Distribusi: {sat_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik untuk satisfaction.")

        if cat_cols:
            loyal_col = st.selectbox("Pilih Kolom Loyalti (categorical)", cat_cols, key="sat_cat")
            vc = df[loyal_col].value_counts().reset_index()
            vc.columns = [loyal_col, "Total"]
            fig = px.bar(vc, x=loyal_col, y="Total", title=f"Distribusi: {loyal_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Tidak ada kolom kategorikal untuk loyalty.")

else:
    st.info("Upload file CSV terlebih dahulu atau letakkan 'df_EDA shopping.csv' di folder project.")
