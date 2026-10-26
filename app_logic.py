import re
import mysql.connector
import pandas as pd
from sklearn.naive_bayes import MultinomialNB

# 1. Feature Extraction: Turning text into numbers
def get_url_features(url):
    features = {
        'length': len(url),
        'dots': url.count('.'),
        'hyphens': url.count('-'),
        'has_at': 1 if '@' in url else 0,
        'is_https': 1 if url.startswith('https') else 0
    }
    return pd.DataFrame([features])

# 2. Mock Training Data (In a real project, load a CSV from Kaggle)
def train_model():
    data = [
        {'url': 'google.com', 'label': 0},
        {'url': 'paypal-verify-secure.biz', 'label': 1},
        {'url': 'facebook.com/login', 'label': 0},
        {'url': 'claim-your-prize-now.tk', 'label': 1}
    ]
    df_train = pd.DataFrame([get_url_features(d['url']).iloc[0] for d in data])
    labels = [d['label'] for d in data]
    
    model = MultinomialNB()
    model.fit(df_train, labels)
    return model

# 3. MySQL Storage Function
def save_to_db(url, label, score):
    conn = mysql.connector.connect(host="localhost", user="root", password="yourpassword", database="linkshield_db")
    cursor = conn.cursor()
    query = "INSERT INTO url_intelligence (url, label, confidence_score) VALUES (%s, %s, %s)"
    cursor.execute(query, (url, label, score))
    conn.commit()
    conn.close()