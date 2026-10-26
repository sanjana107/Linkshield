import pandas as pd
from sklearn.naive_bayes import MultinomialNB
import mysql.connector

# Feature extraction: Turning raw URL strings into numbers
def get_features(url):
    return {
        'len': len(url),
        'dots': url.count('.'),
        'hyphens': url.count('-'),
        'at': 1 if '@' in url else 0,
        'https': 1 if url.startswith('https') else 0
    }

def train_link_model():
    # Example training data - in a real scenario, use a large CSV
    training_data = [
        {"url": "google.com", "label": 0},
        {"url": "secure-login-account.com-verify.info", "label": 1},
        {"url": "amazon.com/orders", "label": 0},
        {"url": "get-free-gift-card-now.tk", "label": 1}
    ]
    df = pd.DataFrame([get_features(d['url']) for d in training_data])
    labels = [d['label'] for d in training_data]
    
    model = MultinomialNB()
    model.fit(df, labels)
    return model