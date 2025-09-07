import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")
st.title("📊 Employee Attrition Dashboard")

# Debugging: show current folder and files
st.write("📂 Current folder:", os.getcwd())
st.write("📄 Files in data folder:", os.listdir("data"))

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/employee_data.csv")
    except FileNotFoundError:
        st.error("❌ 'employee_data.csv' not found. Make sure it's inside the 'data' folder.")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("❌ 'employee_data.csv' is empty. Add data to the CSV.")
        st.stop()

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
department = st.sidebar.multiselect("Department", df["Department"].unique())
education = st.sidebar.multiselect("Education Field", df["EducationField"].unique())

filtered_df = df.copy()
if department:
    filtered_df = filtered_df[filtered_df["Department"].isin(department)]
if education:
    filtered_df = filtered_df[filtered_df["EducationField"].isin(education)]

# KPIs
total_employees = filtered_df.shape[0]
attrition_rate = (filtered_df["Attrition"].value_counts(normalize=True).get("Yes", 0)) * 100
avg_age = int(filtered_df["Age"].mean())
avg_income = int(filtered_df["MonthlyIncome"].mean())

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("👥 Total Employees", total_employees)
kpi2.metric("📉 Attrition Rate (%)", f"{attrition_rate:.1f}")
kpi3.metric("🎂 Average Age", avg_age)
kpi4.metric("💰 Avg Monthly Income", f"${avg_income}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Attrition by Department")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x="Department", hue="Attrition", palette="Set2", ax=ax)
    ax.set_ylabel("Count")
    st.pyplot(fig)

with col2:
    st.subheader("Attrition by Education Field")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x="EducationField", hue="Attrition", palette="Set1", ax=ax)
    ax.set_ylabel("Count")
    st.pyplot(fig)

st.markdown("---")

# Extra charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("Attrition Distribution")
    attr_counts = filtered_df["Attrition"].value_counts()
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(attr_counts, labels=attr_counts.index, autopct="%1.1f%%", startangle=90, colors=["#FF9999","#99CCFF"])
    ax.axis("equal")
    st.pyplot(fig)

with col4:
    st.subheader("Correlation Heatmap")
    numeric_cols = filtered_df.select_dtypes(include=["int64", "float64"])
    if not numeric_cols.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.info("No numeric columns available for correlation.")

st.markdown("---")

# Dataset preview
st.subheader("📄 Employee Dataset")
st.dataframe(filtered_df)
