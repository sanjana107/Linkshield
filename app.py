import streamlit as st
import pandas as pd
import re
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# --- 1. THE WHITELIST ---
# Known safe domains bypass the AI to prevent false positives
WHITELIST = ['linkedin.com','google.com', 'facebook.com', 'microsoft.com', 'amazon.com','amazon.in','apple.com', 'amazon.co.uk']

def is_whitelisted(url):
    # Clean the URL to extract the base domain
    clean_url = url.replace('https://', '').replace('http://', '').replace('www.', '')
    domain = clean_url.split('/')[0]
    return domain.lower() in WHITELIST

# --- 2. FEATURE EXTRACTION ---
def extract_features(url):
    features = {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_at': url.count('@'),
        'is_https': 1 if url.startswith('https') else 0,
        'has_ip': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'suspicious_tld': 1 if any(url.endswith(t) for t in ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.biz', '.info']) else 0
    }
    return features

# --- 3. MODEL TRAINING (CACHED) ---
@st.cache_resource
def train_link_model():
    data = [
        {"url": "google.com", "label": 0},
        {"url": "microsoft.com/secure", "label": 0},
        {"url": "amazon.co.uk", "label": 0},
        {"url": "secure-login-verify.xyz", "label": 1},
        {"url": "update-paypal-account.info", "label": 1},
        {"url": "172.16.254.1/login", "label": 1},
        {"url": "free-gift-cards.tk", "label": 1}
    ]
    df_rows = []
    for d in data:
        f = extract_features(d['url'])
        f['label'] = d['label']
        df_rows.append(f)
    
    df = pd.DataFrame(df_rows)
    X = df.drop('label', axis=1)
    y = df['label']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# --- 4. UI AND LOGIC EXECUTION ---
st.set_page_config(page_title="LinkShield AI", layout="centered")
st.title("🛡️ LinkShield")

# Initialize Model
model = train_link_model()

# User Input (Defined BEFORE the 'if' block to avoid NameError)
url_input = st.text_input("Enter URL to scan:", placeholder="https://check-link-here.com")

if url_input:
    # Check Whitelist first
    if is_whitelisted(url_input):
        prob = 0.0
        label = "✅ VERIFIED SAFE (WHITELISTED)"
        risk_color = "green"
        is_risk = False
    else:
        # AI Prediction for non-whitelisted sites
        feat = extract_features(url_input)
        prob = model.predict_proba(pd.DataFrame([feat]))[0][1] * 100
        
        # 1% Sensitivity Logic
        is_risk = prob >= 1.0 
        label = "🚨 RISK DETECTED" if is_risk else "✅ SAFE"
        risk_color = "red" if is_risk else "green"

    # GAUGE VISUALIZATION
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prob,
        title = {'text': f"Status: {label}"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': risk_color},
            'steps': [
                {'range': [0, 1], 'color': "#e8f5e9"},
                {'range': [1, 100], 'color': "#ffebee"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 1.0
            }
        }
    ))
    st.plotly_chart(fig)

    # Final Text Feedback
    if is_risk:
        st.error(f"**Warning:** High-sensitivity mode triggered. {prob:.2f}% phishing probability.")
    elif prob == 0 and "WHITELIST" in label:
        st.info(f"This domain is a recognized trusted partner.")
    else:
        st.success(f"**Clean:** No malicious patterns detected. (Probability: {prob:.2f}%)")