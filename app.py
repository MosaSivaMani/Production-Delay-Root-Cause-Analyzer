import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Production Delay Analyzer", layout="wide")

st.title("📊 Production Delay Root-Cause Analyzer")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # Parse time if needed
    if not pd.api.types.is_datetime64_any_dtype(df["Timestamp"]):
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Pie chart: delay reasons
    st.subheader("📌 Delay Reasons Breakdown")
    reason_counts = df["Reason for Stop"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(reason_counts, labels=reason_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Line chart: delay over time
    st.subheader("⏱️ Delays Over Time")
    df["Date"] = df["Timestamp"].dt.date
    daily_counts = df.groupby("Date").size()
    fig2, ax2 = plt.subplots()
    daily_counts.plot(kind='line', ax=ax2)
    ax2.set_ylabel("Delays")
    st.pyplot(fig2)

    # Most problematic machine
    st.subheader("⚠️ Machine Causing Most Delays")
    machine_counts = df["Machine ID"].value_counts()
    st.write(f"🛠️ Machine with most delays: **{machine_counts.idxmax()}** ({machine_counts.max()} delays)")
