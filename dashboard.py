import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="LinkShield AI", layout="wide")
st.title("🛡️ LinkShield: AI URL Security Dashboard")

# --- DATABASE CONNECTION ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="yourpassword", database="linkshield_db"
    )

# --- 1. TOP METRICS SECTION ---
conn = get_db_connection()
df_history = pd.read_sql("SELECT * FROM url_intelligence", conn)
conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total URLs Scanned", len(df_history))
col2.metric("Phishing Detected", len(df_history[df_history['label'] == 'PHISHING']))
col3.metric("System Status", "Active", delta="AI Online")

# --- 2. REAL-TIME SCANNER ---
st.subheader("🔍 Scan a New URL")
url_input = st.text_input("Enter URL to analyze:", placeholder="https://example-phish.com")

if url_input:
    # (Simulated prediction logic - replace with your model.predict)
    risk_score = 85 if "-" in url_input else 15 
    label = "PHISHING" if risk_score > 50 else "SAFE"
    
    # Visual Gauge for Risk
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        title = {'text': f"Result: {label}"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "red" if label == "PHISHING" else "green"}}
    ))
    st.plotly_chart(fig)

# --- 3. ANALYTICS SECTION ---
st.divider()
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📈 Threat Distribution")
    type_counts = df_history['label'].value_counts()
    fig_pie = px.pie(values=type_counts.values, names=type_counts.index, hole=0.4)
    st.plotly_chart(fig_pie)

with right_col:
    st.subheader("📋 Recent Intelligence Log (MySQL)")
    st.table(df_history.sort_values('scanned_at', ascending=False).head(5))