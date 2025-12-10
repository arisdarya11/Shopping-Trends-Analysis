import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =================================================
# CONFIG
# =================================================
st.set_page_config(page_title="Customer Analytics Platform", layout="wide")
sns.set_style("whitegrid")

st.title("📊 Customer Analytics Platform")

# =================================================
# SIDEBAR
# =================================================
st.sidebar.title("Navigation")
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

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])


# =================================================
# LOAD FUNCTION
# =================================================
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    df = load_data(uploaded_file)

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # =================================================
    # 1. GENERAL DASHBOARD
    # =================================================
    if menu == "General Dashboard":
        st.header("📈 General Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())
        col4.metric("Numeric Features", len(num_cols))

        st.markdown("---")

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Quick Distribution")

        left, right = st.columns(2)

        with left:
            if num_cols:
                col = st.selectbox("Pilih Numeric Column", num_cols)
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax)
                st.pyplot(fig)

        with right:
            if cat_cols:
                col = st.selectbox("Pilih Categorical Column", cat_cols)
                fig, ax = plt.subplots()
                df[col].value_counts().plot(kind="bar", ax=ax)
                st.pyplot(fig)

    # =================================================
    # 2. EDA
    # =================================================
    elif menu == "EDA":
        st.header("🔍 Exploratory Data Analysis")

        st.subheader("Dataset Overview")
        st.dataframe(df.describe())

        st.subheader("Data Types")
        st.dataframe(pd.DataFrame(df.dtypes, columns=["Tipe Data"]))

        st.subheader("Missing Values")
        st.dataframe(df.isnull().sum())

        if num_cols:
            st.subheader("Boxplot (Outlier Detection)")
            box_col = st.selectbox("Pilih kolom", num_cols)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[box_col], ax=ax)
            st.pyplot(fig)

        if len(num_cols) > 1:
            st.subheader("Correlation Matrix")
            corr = df[num_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)

    # =================================================
    # 3. CUSTOMER DEMOGRAPHICS
    # =================================================
    elif menu == "Customer Demographics":
        st.header("👥 Customer Demographics Dashboard")

        if cat_cols:
            demo_col = st.selectbox("Pilih Kolom Demografi", cat_cols)

            fig, ax = plt.subplots()
            df[demo_col].value_counts().plot(kind="bar", ax=ax)
            ax.set_ylabel("Jumlah Customer")
            st.pyplot(fig)

        if num_cols:
            age_col = st.selectbox("Pilih Numeric Demographic", num_cols)

            fig, ax = plt.subplots()
            sns.histplot(df[age_col], kde=True, ax=ax)
            st.pyplot(fig)

    # =================================================
    # 4. CUSTOMER SPENDING
    # =================================================
    elif menu == "Customer Spending":
        st.header("💰 Customer Spending Insights")

        if num_cols:
            spend_col = st.selectbox("Pilih Kolom Spending", num_cols)

            # KPI
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Spending", f"{df[spend_col].sum():,.0f}")
            c2.metric("Average Spending", f"{df[spend_col].mean():,.2f}")
            c3.metric("Max Spending", f"{df[spend_col].max():,.0f}")

            st.markdown("---")

            fig, ax = plt.subplots()
            sns.histplot(df[spend_col], kde=True, ax=ax)
            st.pyplot(fig)

            if cat_cols:
                seg_col = st.selectbox("Segmentasi Berdasarkan", cat_cols)

                group = df.groupby(seg_col)[spend_col].mean().sort_values(ascending=False)

                fig, ax = plt.subplots()
                group.plot(kind="bar", ax=ax)
                ax.set_ylabel("Rata-rata Spending")
                st.pyplot(fig)

    # =================================================
    # 5. CUSTOMER SATISFACTION & LOYALTY
    # =================================================
    elif menu == "Customer Satisfaction & Loyalty":
        st.header("⭐ Customer Satisfaction & Loyalty")

        if num_cols:
            sat_col = st.selectbox("Pilih Kolom Satisfaction Score", num_cols)

            c1, c2, c3 = st.columns(3)
            c1.metric("Average Score", f"{df[sat_col].mean():.2f}")
            c2.metric("Highest Score", f"{df[sat_col].max():.2f}")
            c3.metric("Lowest Score", f"{df[sat_col].min():.2f}")

            fig, ax = plt.subplots()
            sns.histplot(df[sat_col], kde=True, ax=ax)
            st.pyplot(fig)

        if cat_cols:
            loyal_col = st.selectbox("Pilih Kolom Loyalti", cat_cols)

            fig, ax = plt.subplots()
            df[loyal_col].value_counts().plot(kind="bar", ax=ax)
            ax.set_ylabel("Jumlah Customer")
            st.pyplot(fig)

else:
    st.info("Upload file CSV terlebih dahulu untuk memulai.")

